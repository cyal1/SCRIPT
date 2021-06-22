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
VUL_PATH = "/root.exe"
WAF_STRING = ["已被阻断", "店铺", "拦截ID", "html"]
TIME_OUT = 8
WORKERS = 50
NAME_SERVER = ["223.5.5.5", "8.8.8.8"]
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/89.0.4389.90 Safari/537.36"

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
        "is_ipv6": None,
        "dst_ip": None,
        "waf_detected": None,
        "matched_string": None,
        "status_code": None,
        "final_url": None,
        "requests_error": None,
    }

    try:
        resp = req(
            url=url,
            ipv6=ipv6,
            timeout=TIME_OUT,
            verify=False,
            stream=True,
            allow_redirects=True,
            headers={
                "User-Agent": USER_AGENT
            }
        )
    except Exception as e:
        ret["requests_error"] = e.__class__.__name__
        return ret
    ret["is_ipv6"] = ipv6
    ret["final_url"] = resp.url
    ret["status_code"] = resp.status_code
    dst_ip = resp.raw._connection.sock.getpeername()[0]
    if dst_ip.startswith("::ffff:"):
        dst_ip = dst_ip.replace("::ffff:", "")
    ret["dst_ip"] = dst_ip
    # print(resp.text)
    for key in WAF_STRING:
        if key in resp.text:
            ret["matched_string"] = key
            ret["waf_detected"] = True
            return ret
    ret["waf_detected"] = False
    return ret


proc = subprocess.run(["curl", "-6", "-s", "ifconfig.io"], stdout=subprocess.PIPE)
if ":" not in proc.stdout.decode():
    print("you network not support ipv6, you can get ipv6 through mobile hotspot.")
    exit()

with open(FILE) as f:
    url_list = f.readlines()

# create excel
file_name = time.strftime("%Y-%m-%d-%H-%M-%S.xlsx", time.localtime())
workbook = xlsxwriter.Workbook(file_name)
worksheet = workbook.add_worksheet()
row = 1
col = 0

# excel title
bold = workbook.add_format({'bold': True, "align": "center"})
title = ['origin_url', 'is_ipv6', 'dst_ip', 'waf_detected', 'matched_string', 'status_code', 'final_url',
         'requests_error']
for j, t in enumerate(title):
    worksheet.write(0, j, t, bold)

# TEST_URL_LIST = [
#     "https://www.baidu.com",
#     "https://www.qq.com",
#     "https://www.taobao.com"
# ]

with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
    # future_to_url = {executor.submit(send_req, url.strip(), IPV6): url  for url in TEST_URL_LIST}
    future_to_url = {}

    for url in url_list:
        url = url.strip()
        if not url.startswith("http"):
            url += "http://"
        aaaa_record = getipv6(tldextract.extract(url).fqdn)
        if len(aaaa_record) != 0:
            future_to_url[executor.submit(send_req, url, True)] = aaaa_record
            future_to_url[executor.submit(send_req, url, False)] = aaaa_record
        else:
            future_to_url[executor.submit(send_req, url, False)] = aaaa_record

    for future in concurrent.futures.as_completed(future_to_url):
        aaaa_record = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            # data["AAAA_record"] = aaaa_record
            print(data)
            # write to excel
            for line in data:
                if line == "dst_ip" and data["is_ipv6"] is True and ":" not in data[line]:
                    data[line] = ", ".join(aaaa_record)
                if data[line] is not None:
                    worksheet.write(row, col, data[line])
                col += 1
            col = 0
            row += 1
workbook.close()
print("Saved results to " + file_name)

# with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
#     for result in executor.submit(send_req,URL_LIST):
#         print(result)


# resp = req("https://www.taobao.com/root.exe",stream=True,allow_redirects=True)
# print(resp.raw._connection.sock.getpeername())
