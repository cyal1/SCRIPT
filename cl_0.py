#! python3
import concurrent.futures
import sys
import urllib3
from urllib3 import HTTPConnectionPool, HTTPSConnectionPool
from urllib3.util import parse_url

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 " \
     "Safari/537.36 "


def detect_cl_0(url):
    u = parse_url(url)
    target = ""
    if u.scheme is not None:
        target += u.scheme + u"://"
    if u.auth is not None:
        target += u.auth + u"@"
    if u.host is not None:
        target += u.host
    if u.port is not None:
        target += u":" + str(u.port)
    target += path
    http = urllib3.PoolManager()
    try:
        r = http.urlopen(method="GET",
                         url=target,
                         redirect=False,
                         retries=0,
                         timeout=5,
                         body="body",
                         headers={
                             "Content-Length": "20",
                             "User-Agent": UA,
                         })
    except Exception as e:
        print(target, e.reason)
    else:
        scheme, host, port = r._pool.scheme, r._pool.host, r._pool.port
        if scheme == 'https':
            conn = HTTPSConnectionPool(host, port)
        else:
            conn = HTTPConnectionPool(host, port)
        attacker = conn.urlopen(method="GET",
                                url=path,
                                redirect=False,
                                retries=0,
                                timeout=5,
                                body="body",
                                headers={
                                    "Connection": "keep-alive",
                                    "User-Agent": UA,
                                })
        victim = conn.urlopen(method="GET",
                              url="/",
                              redirect=False,
                              retries=0,
                              timeout=5,
                              headers={
                                  "User-Agent": UA,
                              })

        if attacker.status != victim.status and victim.status != 200:
            print("=" * 10)
            print(target, "cl.0 detected", attacker.status, victim.status)
            print("=" * 10)
        else:
            print(target, "no cl_0")


path = '/favicon.ico'
if len(sys.argv) > 1:
    path = sys.argv[1]

with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(detect_cl_0, url): url.strip() for url in sys.stdin}
    # for future in concurrent.futures.as_completed(future_to_url):
    #     url = future_to_url[future]
    #     try:
    #         data = future.result()
    #     except Exception as exc:
    #         print('%r generated an exception: %s' % (url, exc))
    #     else:
    #         print('%r page is %d bytes' % (url, len(data)))
