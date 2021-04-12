#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:Cyan

"""
Try copying the cluttered IP range contents below to the file and use:
python3 ipParse.py -f filename --smart

192.168.1.0 192.168.2.1/24,192.168.3.4-7,192.168.5.1-.192.168.5.34、192.176.34.6\26、192.187.34.2-67，192.111.111.111，192.168.5.1 - 192.168.5.34 192.168.5.1. -- 0192.168.5.34,192.168.5.1--192.168.5.34、1.2.4.5、192.168.5.5-9
192.168.5.1~192.168.5.34,192.168.5. 1 ~ 192.168.05.0 123.3.3.3. 192.168.5.1~56 192.168.7.1
"""
import requests
from gevent import monkey; monkey.patch_socket()
from gevent.pool import Pool
import gevent
import re
import argparse
import ipaddress
import json
import dns.resolver
import urllib
import socket

requests.packages.urllib3.disable_warnings()


REG_CD = re.compile(
    r'(?P<cd>((([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5]))\.){3})(?P<c1>(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5])))-(?P<c2>(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5])))$')
REG_SUBNET = re.compile(
    r'((([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5]))\.){3}(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5]))\/([0-9]|[1-2][0-9]|3[0-2])$')
REG_IP = re.compile(
    r'((([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5]))\.){3}(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5]))$')
REG_IPRANGE = re.compile(
    r'(?P<bd>((([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5]))\.){2})(?P<c1>(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5])))\.(?P<d1>(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5])))-(?P=bd)(?P<c2>(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5])))\.(?P<d2>(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5])))$')


def replSpace(rep):
    return rep.group().replace(' ', '')


def replPoint(rep):
    return rep.group().strip('.')


def replZero(rep):
    return rep.group().lstrip('0')

# IPLIST = []
# 保存并去重
# def save(ip):
#     if ip not in IPLIST:
#         IPLIST.append(ip)

# 处理 192.168.1.1-192.168.2.128 形式
def ipRange(item):
    r=[]
    res = REG_IPRANGE.match(item)
    bd = res.group('bd')
    c1 = int(res.group('c1'))
    c2 = int(res.group('c2'))
    d1 = int(res.group('d1'))
    d2 = int(res.group('d2'))
    if c1 == c2:
        if d1 < d2:
            for i in range(d1, d2 + 1):
                r.append(bd + str(c1) + '.' + str(i))
        else:
            print(f'\033[1;31m请检查你的IP:{item}\033[0m')
    elif c1 < c2:
        for c in range(c1, c2 + 1):
            for d in range(d1, 255):
                if c == c2 and d > d2:
                    break
                else:
                    r.append(bd + str(c) + '.' + str(d))
            d1 = 0
    else:
        print(f'\033[1;31m请检查你的IP:{item}\033[0m')
    return r

# 处理 192.168.2.1-243 形式
def dealCd(item):
    r=[]
    res = REG_CD.match(item)
    cd = res.group('cd')
    c1 = int(res.group('c1'))
    c2 = int(res.group('c2'))
    if c1 < c2:
        for i in range(c1, c2 + 1):
            r.append(cd + str(i))
    else:
        print(f'\033[1;31m请检查你的IP:{item}\033[0m')
    return r
# 处理 192.168.1.0/24 形式
def dealSubnet(item):
    r=[]
    if int(re.match(r'.*/(\d+)',item).group(1))<=16:
        print(f'too big range:{item}')
        exit()
    net = ipaddress.ip_network(item, strict=False)
    for ip in net.hosts():
        r.append(str(ip))
    return r

# 将不同形式的 IP 交给不同的方法处理
def ipParse(iplist):
    IPLIST=[]
    for item in iplist:
        # print(item)
        if REG_IPRANGE.match(item):  # 192.168.1.1-192.168.2.128
            IPLIST.extend(ipRange(item))
        elif REG_CD.match(item):  # 192.168.2.1-243
            IPLIST.extend(dealCd(item))
        elif REG_SUBNET.match(item): # 192.168.2.1/24
            IPLIST.extend(dealSubnet(item))
        elif REG_IP.match(item):
            IPLIST.append(item)
        else:
            print(f'\033[1;31m请检查你的IP:{item}\033[0m')
    r = list(set(IPLIST))
    r.sort(key=IPLIST.index)
    return r

# 处理无格式 IP 范围文件
def smart(ipfile):
    with open(ipfile, encoding="utf-8") as f:
        content = f.read()
    print("-" * 80)
    # 192.168.1.1 -- 254 将不规范的分割符（如： ~~ ~ -- -）全部替换成-,\替换成/
    s1 = re.sub(r'\s*[-~]+\s*', '-', content).replace('\\','/').replace('"','').replace("'",'')
    # 123. 34 .123 . 123 去掉之间多余的空格    -- 如果出错，请注释此行
    s1 = re.sub(r'(\d+\s*\.\s*){3}\d+', replSpace, s1)
    # .123.123.123.123 去掉左右两边误写的.    -- 如果出错，请注释此行
    s1 = re.sub(r'\.?(\d+\.*){3}\d+\.?', replPoint, s1)
    s1 = re.sub(r'\d{2,}', replZero, s1)  # 去掉 123.0.02.1 中 0 开头的多位数
    s1 = re.split(r'[\n\s,，、;；]+', s1) # 以这些符号分隔成列表并去重
    s1 = list({x for x in s1 if x !=''})  
    s1.sort()
    print(s1)
    print("-" * 80)
    for x in ipParse(s1):
        print(x)

def ip_location(ip):
    try:
        url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query="+ip+"&co=&resource_id=5809&t=1600743020566&ie=utf8&oe=gbk&cb=op_aladdin_callback&format=json&tn=baidu&cb=jQuery110208008102506768224_1600742984815&_=1600742984816"
        resp=requests.get(url)
        # print(resp.text)
    except Exception as e:
        # print(e)
        return "Error: "+str(e)
    j=json.loads(resp.text[42:-1])
    if len(j['Result'])!=0:
        # print(j['Result'][0]['DisplayData']['resultData']['tplData']['location'])
        return j['Result'][0]['DisplayData']['resultData']['tplData']['location']
    else:
        # print(f"INFO: {ip} {j}")
        # print(j['Result'])
        return j['Result']

def ip_reverse(ip):
    # https://www.threatcrowd.org/searchApi/v2/ip/report/?ip=
    try:
        resp=requests.get(f"https://www.threatcrowd.org/searchApi/v2/ip/report/?ip={ip}&__cf_chl_jschl_tk__=b23e1ebddba7a8afcec8002ebe8161982a307678-1600841853-0-AdBviI4eBSvsCtV19ogQiOgQh8BZDLUSjLLWlPxcUmToHHMVBUzRMOttXDt0rU_oBQ9sjEco0JVg1HpkyolfayL92SM2O7_7QPM67RLnKw6bB2HLrDSbAe1isBru5CZQMW37d1m5MI-3maLEyCwpAx5M5n3gjSTPATv6XUK6GYvSdIIflKHKr8NI1wjWqe6YHdsdGshphzA5RP9IINVQ_q3mRfxz7YbZiW49E3sduJLtQjiFB1IaGapMdW_HMt_qbw_jJo4S7j_w-ZnEVKTCBpwR5LVACjy3p2rv_lTL7Uw1zW1J84fJ--sTRfKa1iZlN1-eENeG293SoP0IIGM0l-c",
            timeout=10,
            cookies={"__cfduid":"d1f527bf2b91e30ae3e5edc6392e873091600248379","cf_clearance":"1d01f377dd9b8c5c7b76a488c7b4adbd3da6055a-1600841859-0-1zd74c2a3az56d45067z127237b9-150"},
            headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"},
            verify=False,
            )
    except Exception as e:
        print(f"Please manual access: https://www.threatcrowd.org/searchApi/v2/ip/report/?ip={ip}")
        return e
    # print(resp.text)
    try:
        j=json.loads(resp.text)
    except Exception as e:
        print(f"Please manual access: https://www.threatcrowd.org/searchApi/v2/ip/report/?ip={ip}")
        return "Cloudflare DDos Detect!"
    r=""
    if j['response_code']!='0':
        if len(j['resolutions'])>100:
            j['resolutions']=j['resolutions'][:99]
        for record in j['resolutions']:
            r+=f"{record['last_resolved']}\t{record['domain']}\n"
        return r[:-1]
    else:
        # print("Not Found!")
        return "Not found any reverse information!"

def interactive_ip_reverse():
    """
    interactive of ip reverse
    """
    while True:
        ip=input("Input IP: ").strip()
        if not re.match(r"^(\d{1,3}\.){3}\d{1,3}$",ip):
            print("\"%s\" is not a valid IP!"%ip)
            print("-"*100)
            continue
        jobs=[
                # gevent.spawn(ip_location, ip),
                gevent.spawn(ip_reverse, ip),
        ]
        gevent.joinall(jobs)
        for job in jobs:
            print(job.value)
        print("-"*100)

def extract_host(url):
    url=url.strip()
    if (not url.startswith("http") and not url.startswith("//")):
        url="https://"+url

    # print(urllib.parse.urlparse(url)[1])
    return urllib.parse.urlparse(url)[1]

my_resolver = dns.resolver.Resolver()
my_resolver.nameservers = ['8.8.8.8']

def getIP(url):
    host=extract_host(url)
    try:
       google_record=[rdata.address for rdata in my_resolver.resolve(host, 'A')]
    except Exception as e:
        # print(f"\033[1;31m ERROR: {host} resolve error: {e.__class__.__name__}\033[0m")
        google_record=[]
    try:
        socket_record=socket.gethostbyname_ex(host)[2]
    except Exception as e:
        # print(f"\033[1;31m ERROR: {host} resolve error: {e.__class__.__name__}\033[0m")
        socket_record=[]
    # print(google_record,socket_record)
    socket_record.extend([x for x in google_record if x not in socket_record])
    # print(google_record,socket_record)
    if len(socket_record) == 0:
        print(f"\033[1;31m ERROR: {host} resolve error\033[0m")
    return host,socket_record

def sync_getIP(url_list):
    r=[]
    p=Pool(THREADS)
    threads=[p.spawn(getIP, i) for i in url_list]
    gevent.joinall(threads)
    for item in threads:
        r.append(item.value)
    return r

def archive(domain_list):
    sigleIP={}
    info_pool=[]
    for host,ip_list in sync_getIP(domain_list):
        info_pool.append((host,ip_list))
        if len(ip_list)==1:
            sigleIP[ip_list[0]]=[]
    # for ip in sigleIP:
    #     print("### "+ip)
    #     for info in info_pool:
    #         if ip in info[2]:
    #             print(info[1])
    for info in info_pool:
        for ip in info[1]:
            if ip in sigleIP.keys():
                sigleIP[ip].append(info[0])
                break
        else:
            print(info[0],info[1])
    # print(sigleIP)
    for i,v in sigleIP.items():
        print(f"### {i}\t"+ip_location(i))
        for t in v:
            print(t)
    print("### Nmap")
    print(f"sudo nmap -Pn -sS -sV -T3 -p1-65535 --open {' '.join([ip for ip in sigleIP.keys()])}")

def sync_ip_location(ip_list):
    ##iplocation sync
    loc=lambda ip:(ip,ip_location(ip))
    p=Pool(THREADS)
    threads=[p.spawn(loc, i) for i in ip_list]
    gevent.joinall(threads)
    for item in threads:
        print(item.value[0],item.value[1])
    # for i in ip_list:
    #     if args.location:
    #         print(i,ip_location(i))
    #     else:
    #         print(i)
    print(f'\033[0;36m共{len(ip_list)}个IP\033[0m')

THREADS=None
def main():
    parser = argparse.ArgumentParser("For ip list:")
    ip_parser=parser.add_argument_group("For IP list")
    # parser.description = 'Parse IP range like 192.168.2.3/26 10.0.4.1-10.0.4.9 10.0.0.1-254'
    group = parser.add_mutually_exclusive_group()
    domain_parser=parser.add_argument_group("For domain list")
    reverse_parser=parser.add_argument_group("Reverse IP")
    group.add_argument("-f", '--file', help="The file containing a list of IPs or domains")
    group.add_argument("-c", '--cidr', help="Command line read a domains,IP or CIDR like 192.168.2.3/26,10.0.0.1-254,10.0.4.1-10.0.4.9")
    ip_parser.add_argument('--location', action="store_true", help="The location of IP")
    parser.add_argument('-t', "--threads", type=int, default=20, help="Number of threads（default 20）")
    ip_parser.add_argument('--smart', action="store_true", help="Automatic analysis of messy file containing IPs")
    domain_parser.add_argument('--ip', action="store_true", help="show IP of domain")
    reverse_parser.add_argument('--interactive', action="store_true", help="open an interactive to get domain history of IP")
    domain_parser.add_argument('--archive', action="store_true", help="Archive IP and domain")
    args = parser.parse_args()
    if args.interactive:
        interactive_ip_reverse()
    if not args.file and not args.cidr:
        print("The argument requires the -f or -c")
        exit(1)
    if args.archive and not args.ip:
        print("The --archive argument requires the --ip")
        exit(1)
    if args.smart and not args.file:
        print("The --smart argument requires the -f or --file")
        exit(1)
    global THREADS
    THREADS=args.threads
    if args.ip:
        if args.file:
            if args.archive:
                # python3 iptool.py -f domain_list.txt --ip --archive
                with open(args.file, encoding="utf-8") as f:
                    archive(f.readlines())
            else:
                # python3 iptool.py -f domain_list.txt --ip
                with open(args.file, encoding="utf-8") as f:
                    for x,y in sync_getIP(f.readlines()):
                        print(x,y)
        else:
            # python3 iptool.py -c www.baidu.com,www.qq.com --ip
            url_list=args.cidr.strip(',').split(',')
            for u in url_list:
                host,ip_list=getIP(u)
                print(host)
                for ip in  ip_list:
                    print(ip,ip_location(ip))
    elif args.file:
        if args.smart:
            # python3 iptool.py -f ip_or_CIDR_messy_list.txt
            smart(args.file)
        else:
            with open(args.file, encoding="utf-8") as f:
                ip_list=[i.strip() for i in f if i.strip() !='']
                # ip.sort()
            if args.location:
                # python3 iptool.py -f ip_or_CIDR_list.txt --location
                sync_ip_location(ipParse(ip_list)) # 异步处理
            else:
                for x in ipParse(ip_list):
                        # python3 iptool.py -f ip_or_CIDR_list.txt
                        print(x)
    elif args.cidr:
        ip_list=ipParse(args.cidr.strip(',').split(','))
        # python3 iptool.py -c 192.168.0.1/24 --location
        if args.location:
            sync_ip_location(ip_list) # 异步处理
        else:
            for x in ip_list:
                    # python3 iptool.py -c 192.168.0.1/24
                    print(x)
    else:
        print('Use -h to show help')

if __name__ == '__main__':
    main()
