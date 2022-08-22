#! python3
import concurrent.futures
import sys
import urllib3
from urllib3 import HTTPConnectionPool, HTTPSConnectionPool
from urllib3.util import parse_url

urllib3.disable_warnings()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 " \
     "Safari/537.36 "


def detect_cl_0(url, path=None):
    u = parse_url(url)
    if path is None:
        path = u.path if u.path is not None else '/'
    target = u.scheme + "://" + u.host
    if u.port is not None:
        target += ':' + str(u.port)
    target += path
    if u.scheme == 'https':
        conn = HTTPSConnectionPool(u.host, u.port if u.port is not None else 443, cert_reqs='CERT_NONE',
                                   assert_hostname=False)
    else:
        conn = HTTPConnectionPool(u.host, u.port if u.port is not None else 80)
    try:
        base_req = conn.urlopen(method=victim_method,
                                url=path,
                                redirect=False,
                                retries=0,
                                timeout=timeout,
                                headers={
                                    "User-Agent": UA
                                })
    except Exception as e:
        print(url, e)
        # pass
    else:
        base_status, base_len = base_req.status, len(base_req.data)
        attacker = conn.urlopen(method=attacker_method,
                                url=path,
                                redirect=False,
                                retries=0,
                                timeout=timeout,
                                body=smuggle_data,
                                headers={
                                    # "Content-Length": "10",
                                    "Connection": "keep-alive",
                                    "User-Agent": UA
                                })
        victim = conn.urlopen(method=victim_method,
                              url=path,
                              redirect=False,
                              retries=0,
                              timeout=timeout,
                              headers={
                                  "User-Agent": UA
                              })

        if base_status != victim.status:
            print(
                f"\033[91m{target}, baseline:{base_status, base_len}, attacker:{attacker.status, len(victim.data)}, "
                f"victim:{victim.status, len(victim.data)}, CL.0 detected!\033[0m")
            print("HTTP/" + str(victim.version / 10), victim.status, victim.reason)
            print('\r\n'.join([k + ': ' + victim.headers[k] for k in victim.headers]))
            print(f"\r\n{victim.data.decode()}")

        elif base_len != len(victim.data):
            print(
                f"\033[93m{target}, baseline:{base_status, base_len}, attacker:{attacker.status, len(victim.data)}, "
                f"victim:{victim.status, len(victim.data)}, CL.0 detected!\033[0m")
        else:
            pass
            print(
                f"{target}, baseline:{base_status, base_len}, attacker:{attacker.status, len(victim.data)}, "
                f"victim:{victim.status, len(victim.data)}, CL.0 Not Found")
    finally:
        conn.close()


victim_method = "GET"
attacker_method = "GET"
smuggle_data = "a b %" # body
timeout = 35
endpoint = '/favicon.ico'  # set endpoint None to use the url path.  /static/css/*.css , redirect / /en , /../

if len(sys.argv) > 1:
    if sys.argv[1].startswith('http'):
        detect_cl_0(sys.argv[1])
        exit(0)
    else:
        endpoint = sys.argv[1]

if sys.stdin.isatty():
    print("""
Usage:
    1. cat urls.txt|python3 cl_0.py   # default use /favicon.ico
    2. cat urls.txt|python3 cl_0.py /robots.txt 
    3. python3 cl_0.py https://www.example.com/static/index.css
        """)
    exit()

with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    future_to_url = {executor.submit(detect_cl_0, url.strip(), endpoint): url.strip() for url in sys.stdin}
