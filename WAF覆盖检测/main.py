import concurrent.futures
import socket
import subprocess
import requests
import urllib3
import dns.resolver
import tldextract
import xlsxwriter
import time

requests.packages.urllib3.disable_warnings()

########################################## config #######################################################

FILE = "./urls.txt"
VUL_PATH = "/0706.exe/?id=1\"%20and%20\"1\"=\"1"
WAF_STRING = ["您的访问请求可能对网站造成安全威胁"]
TIME_OUT = 8
WORKERS = 10
FOLLOW_REDIRECTS = True
NAME_SERVER = ["223.5.5.5", "8.8.8.8"]
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/89.0.4389.90 Safari/537.36"

def waf_func(resp, ret):
    print(resp.content.decode("utf8"))
    for key in WAF_STRING:
        if key in resp.content.decode("utf8"):
            ret["matched_string"] = key
            ret["waf_detected"] = True
            return ret
    ret["waf_detected"] = False
    return ret

#########################################################################################################


def getipv6(domain):
    ret = []
    try:
        my_resolver = dns.resolver.Resolver()
        my_resolver.nameservers = NAME_SERVER
        AAAA_recorder = my_resolver.resolve(domain, 'AAAA')
        for i in AAAA_recorder.response.answer:
            for j in i.items:
                if j.rdtype == 28:
                    ret.append(j.address.replace("\n", " "))
    except Exception:
        pass
    return ret

def getipv4(domain):
    ret = []
    try:
        my_resolver = dns.resolver.Resolver()
        my_resolver.nameservers = NAME_SERVER
        AAAA_recorder = my_resolver.resolve(domain, 'A')
        for i in AAAA_recorder.response.answer:
            for j in i.items:
                if j.rdtype == 1:
                    ret.append(j.address.replace("\n", " "))
    except Exception:
        pass
    return ret


def req(url, ipv6=True, **keywords):
    def allowed_gai_family():
        family = socket.AF_INET
        if ipv6:
            family = socket.AF_INET6
        return family

    urllib3.util.connection.allowed_gai_family = allowed_gai_family

    return requests.get(url, **keywords)


def send_req(url, ipv6=True):
    url = url.rstrip("/") + VUL_PATH
    ret = {
        "origin_url": url,
        "is_ipv6": ipv6,
        "sock_ip": None,
        "waf_detected": None,
        "matched_string": None,
        "status_code": None,
        "requests_error": None,
        "ns_record": None,
        "final_url": None,
    }

    try:
        resp = req(
            url=url,
            ipv6=ipv6,
            timeout=TIME_OUT,
            verify=False,
            stream=True,
            allow_redirects=FOLLOW_REDIRECTS,
            headers={
                "User-Agent": USER_AGENT
            }
        )
        sock_ip = resp.raw._connection.sock.getpeername()[0]
    except AttributeError:
        sock_ip = None
        ret["ns_record"] = ",".join(getipv6(tldextract.extract(url).fqdn)) if ipv6 else ",".join(getipv4(tldextract.extract(url).fqdn))
    except Exception as e:
        ret["ns_record"] = ",".join(getipv6(tldextract.extract(url).fqdn)) if ipv6 else ",".join(getipv4(tldextract.extract(url).fqdn))
        ret["requests_error"] = e.__class__.__name__
        return ret
    ret["is_ipv6"] = ipv6
    ret["final_url"] = resp.url
    ret["status_code"] = resp.status_code
    ret["sock_ip"] = sock_ip
    if sock_ip is not None and ipv6 is True and sock_ip.startswith("::ffff:"): # https://www.taobao.com/root.exe
        ret["ns_record"] = ",".join(getipv6(tldextract.extract(url).fqdn))
    
    return waf_func(resp, ret)

def writeExcel(future_results):

    # create excel
    file_name = time.strftime("%Y-%m-%d-%H-%M-%S.xlsx", time.localtime())
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    # excel title
    bold = workbook.add_format({'bold': True, "align": "center"})
    title = ['origin_url', 'is_ipv6', 'sock_ip', 'waf_detected', 'matched_string', 'status_code', 
             'requests_error', 'ns_record', 'final_url']
    for j, t in enumerate(title):
        worksheet.write(0, j, t, bold)

    # write to excel
    row = 1
    col = 0
    for future in future_results:
        try:
            data = future.result()
        except Exception as exc:
            print('Exception: %s' % exc)
        else:
            print(data)
            for line in data:
                if data[line] is not None:
                    worksheet.write(row, col, data[line])
                col += 1
            col = 0
            row += 1

    workbook.close()
    print("Saved results to " + file_name)


if __name__ == "__main__":
    # print(send_req("http://ip.sb",True))
    # print(send_req("http://ip.sb",False))

    with open(FILE) as f:
        url_list = f.readlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:

        # ipv4 checking...
        future_to_url = {}

        for url in url_list:
            url = url.strip()
            future_to_url[executor.submit(send_req, url, False)] = url
        future_results = concurrent.futures.as_completed(future_to_url)

        # ipv6 checking...
        proc = subprocess.run(["curl", "-6", "-s", "ifconfig.io"], stdout=subprocess.PIPE)
        if ":" not in proc.stdout.decode():
            print("Your network not support ipv6, it will detect ipv4 only. you can get ipv6 through mobile hotspot.\n")
            writeExcel(future_results)
            exit()
        for url in url_list:
            url = url.strip()
            aaaa_record = getipv6(tldextract.extract(url).fqdn) # TODO: 实现多线程
            if len(aaaa_record) != 0:
                future_to_url[executor.submit(send_req, url, True)] = url
        future_results = concurrent.futures.as_completed(future_to_url)
        writeExcel(future_results)
