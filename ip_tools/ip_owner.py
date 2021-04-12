import requests
import re
import sys
import os


# url = "http://ipwhois.cnnic.cn/bns/query/Query/ipwhoisQuery.do?txtquery=111.225.217.41&queryOption=ipv4"



if not os.path.exists(sys.argv[1]):
	try:
		url = "http://ipwhois.cnnic.cn/bns/query/Query/ipwhoisQuery.do?txtquery=%s&queryOption=ipv4"%sys.argv[1]
		# print(url)
		resp = requests.get(url,timeout=3)
	except:
		print("request error")
		sys.exit()
	# print(resp.text)
	obj = re.findall(r' *<td align="left" class="t_blue"><font size="2">(.*)</font></td> *',resp.text.replace("&nbsp",""))
	for o in obj:
		print(o)
else:

	with open(sys.argv[1]) as f:
		l = f.readlines()
	# print(l)


	for ip in l:
		print(ip.strip())
		try:
			url = "http://ipwhois.cnnic.cn/bns/query/Query/ipwhoisQuery.do?txtquery=%s&queryOption=ipv4"%ip.strip()
			print(url)
			resp = requests.get(url,timeout=3)
		except:
			continue
		# print(resp.text)
		obj = re.findall(r' *<td align="left" class="t_blue"><font size="2">(.*)</font></td> *',resp.text.replace("&nbsp",""))
		for o in obj:
			print(o)
