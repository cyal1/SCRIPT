#!/usr/bin/env python
# coding: utf-8
from SocketServer import BaseRequestHandler, ThreadingUDPServer
from cStringIO import StringIO
import os
import socket
import struct
import time

'''
A simple DNS proxy server, support wilcard hosts, IPv6, cache. Usage:

Edit /etc/hosts, add:
    127.0.0.1 *.local
    2404:6800:8005::62 *.blogspot.com
startup dnsproxy(here use Google DNS server as delegating server):
$ sudo python dnsproxy.py -s 8.8.8.8

Then set system dns server as 127.0.0.1, you can verify it by dig:
$ dig test.local

The result should contains 127.0.0.1.

author: marlonyao<yaolei135@gmail.com>
'''
def main():
    import optparse, sys
    parser = optparse.OptionParser()
    parser.add_option('-f', '--hosts-file', dest='hosts_file', metavar='<file>', default='/etc/hosts', help='specify hosts file, default /etc/hosts')
    parser.add_option('-H', '--host', dest='host', default='127.0.0.1', help='specify the address to listen on')
    parser.add_option('-p', '--port', dest='port', default=53, type='int', help='specify the port to listen on')
    parser.add_option('-s', '--server', dest='dns_server', metavar='SERVER', help='specify the delegating dns server')
    parser.add_option('-C', '--no-cache', dest='disable_cache', default=False, action='store_true', help='disable dns cache')

    opts, args = parser.parse_args()
    if not opts.dns_server:
        parser.print_help()
        sys.exit(1)
    dnsserver = DNSProxyServer(opts.dns_server, disable_cache=opts.disable_cache, host=opts.host, port=opts.port, hosts_file=opts.hosts_file)
    dnsserver.serve_forever()

class Struct(object):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

def parse_dns_message(data):
    message = StringIO(data)
    message.seek(4)     # skip id, flag
    c_qd, c_an, c_ns, c_ar = struct.unpack('!4H', message.read(8))
    # parse question
    question = parse_dns_question(message)
    for i in range(1, c_qd):    # skip other question
        parse_dns_question(message)
    records = []
    for i in range(c_an+c_ns+c_ar):
        records.append(parse_dns_record(message))
    return Struct(question=question, records=records)

def parse_dns_question(message):
    qname = parse_domain_name(message)
    qtype, qclass = struct.unpack('!HH', message.read(4))
    end_offset = message.tell()
    return Struct(name=qname, type_=qtype, class_=qclass, end_offset=end_offset)

def parse_dns_record(message):
    parse_domain_name(message)      # skip name
    message.seek(4, os.SEEK_CUR)    # skip type, class
    ttl_offset = message.tell()
    ttl = struct.unpack('!I', message.read(4))[0]
    rd_len = struct.unpack('!H', message.read(2))[0]
    message.seek(rd_len, os.SEEK_CUR)     # skip rd_content
    return Struct(ttl_offset=ttl_offset, ttl=ttl)

def _parse_domain_labels(message):
    labels = []
    len = ord(message.read(1))
    while len > 0:
        if len >= 64:   # domain name compression
            len = len & 0x3f
            offset = (len << 8) + ord(message.read(1))
            mesg = StringIO(message.getvalue())
            mesg.seek(offset)
            labels.extend(_parse_domain_labels(mesg))
            return labels
        else:
            labels.append(message.read(len))
            len = ord(message.read(1))
    return labels

def parse_domain_name(message):
    return '.'.join(_parse_domain_labels(message))

def addr_p2n(addr):
    try:
        return socket.inet_pton(socket.AF_INET, addr)
    except:
        return socket.inet_pton(socket.AF_INET6, addr)

DNS_TYPE_A = 1
DNS_TYPE_AAAA = 28
DNS_CLASS_IN = 1

class DNSProxyHandler(BaseRequestHandler):
    def handle(self):
        reqdata, sock = self.request
        req = parse_dns_message(reqdata)
        q = req.question
        if q.type_ in (DNS_TYPE_A, DNS_TYPE_AAAA) and (q.class_ == DNS_CLASS_IN):
            for packed_ip, host in self.server.host_lines:
                if q.name.endswith(host):
                    # header, qd=1, an=1, ns=0, ar=0
                    rspdata = reqdata[:2] + '\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00'
                    rspdata += reqdata[12:q.end_offset]
                    # answer
                    rspdata += '\xc0\x0c'   # pointer to domain name
                    # type, 1 for ip4, 28 for ip6
                    if len(packed_ip) == 4:
                        rspdata += '\x00\x01'   # 1 for ip4
                    else:
                        rspdata += '\x00\x1c'   # 28 for ip6
                    # class: 1, ttl: 2000(0x000007d0)
                    rspdata += '\x00\x01\x00\x00\x07\xd0'
                    rspdata += '\x00' + chr(len(packed_ip)) # rd_len
                    rspdata += packed_ip
                    sock.sendto(rspdata, self.client_address)
                    return

        # lookup cache
        if not self.server.disable_cache:
            cache = self.server.cache
            cache_key = (q.name, q.type_, q.class_)
            cache_entry = cache.get(cache_key)
            if cache_entry:
                rspdata = update_ttl(reqdata, cache_entry)
                if rspdata:
                    sock.sendto(rspdata, self.client_address)
                    return
        rspdata = self._get_response(reqdata)
        if not self.server.disable_cache:
            cache[cache_key] = Struct(rspdata=rspdata, cache_time=int(time.time()))
        sock.sendto(rspdata, self.client_address)

    def _get_response(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket for the remote DNS server
        sock.connect((self.server.dns_server, 53))
        sock.sendall(data)
        sock.settimeout(60)
        rspdata = sock.recv(65535)
        sock.close()
        return rspdata

def update_ttl(reqdata, cache_entry):
    rspdata, cache_time = cache_entry.rspdata, cache_entry.cache_time
    rspbytes = bytearray(rspdata)
    rspbytes[:2] = reqdata[:2]          # update id
    current_time = int(time.time())
    time_interval = current_time - cache_time
    rsp = parse_dns_message(rspdata)
    for record in rsp.records:
        if record.ttl <= time_interval:
            return None
        rspbytes[record.ttl_offset:record.ttl_offset+4] = struct.pack('!I', record.ttl-time_interval)
    return str(rspbytes)

def load_hosts(hosts_file):
    'load hosts config, only extract config line contains wildcard domain name'
    def wildcard_line(line):
        parts = line.strip().split()[:2]
        if len(parts) < 2: return False
        if not parts[1].startswith('*'): return False
        try:
            packed_ip = addr_p2n(parts[0])
            return packed_ip, parts[1][1:]
        except:
            return None
    with open(hosts_file) as hosts_in:
        hostlines = []
        for line in hosts_in:
            hostline = wildcard_line(line)
            if hostline:
                hostlines.append(hostline)
        return hostlines

class DNSProxyServer(ThreadingUDPServer):
    def __init__(self, dns_server, disable_cache=False, host='127.0.0.1', port=53, hosts_file='/etc/hosts'):
        self.dns_server = dns_server
        self.hosts_file = hosts_file
        self.host_lines = load_hosts(hosts_file)
        self.disable_cache = disable_cache
        self.cache = {}
        ThreadingUDPServer.__init__(self, (host, port), DNSProxyHandler)

if __name__ == '__main__':
    main()

