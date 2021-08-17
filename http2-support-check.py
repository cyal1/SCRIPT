# from hyper import HTTPConnection

# conn = HTTPConnection('www.taobao.com:443')
# conn.request('GET', '/')
# resp = conn.get_response()
# print(resp._stream.__dict__)

import requests
from hyper.contrib import HTTP20Adapter
import concurrent.futures
import sys

with open(sys.argv[1]) as f:
    url_list = f.readlines()


header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
def load_url(url, timeout):
	s = requests.Session()
	s.mount(url, HTTP20Adapter())
	r = s.get(url, timeout=timeout, headers=header)
	return str(r.raw).split(".", 2)[1]

    

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers = 20) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url.strip(), 8): url.strip() for url in url_list}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result() 
        except Exception as exc:
        	pass
            # print('%r generated an exception: %s' % (url, exc))
        else:
        	if data == 'http20':
        		print(url)
