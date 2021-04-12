import concurrent.futures
import socket
import requests_wrapper as requests  # Use this load the patch



URLS = ["https://app2.test.com"]

l = []
with open("/tmp/u.txt") as f:
    l=f.readlines()
header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}

# Retrieve a single page and report the URL and contents
def load_url(url):
    url = url.strip()
    if url.startswith("http"):
        # print(url)
        try:
            resp=requests.get(url+"/wls-wsat/CoordinatorPortType",family=socket.AF_INET6,timeout=10,verify=False,headers=header).text
        except Exception as e:
            print(e)
            return url,""
        if "<title>无法显示此网页</title>" in resp:
            return url,"是"
        # print(resp)
        return url,""
    else:
        return url,""
    # url=url.strip()
    # try:
    #     res = os.popen("echo %s |httpx -title -follow-redirects -path \"/wls-wsat/CoordinatorPortType\" -no-color -silent"%url).read().strip()
    # except Exception as e:
    #     # print(e)
    #     return url + "\t" + "gbk title"
    # return url + "\t" + res

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    # Start the load operations and mark each future with its URL
    for x in executor.map(load_url, l):
        print(x)
    # for future in concurrent.futures.as_completed(future_to_url):
    #     url = future_to_url[future]
    #     # try:
    #     data = future.result()
    #     # except Exception as exc:
    #     #     print('%r generated an exception: %s' % (url, exc))
    #     # else:
    #     #     print('%r page is %d bytes' % (url, len(data)))
    #     print(data)

