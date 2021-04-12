import tldextract
import sys

if __name__ == '__main__':
	if len(sys.argv)!=2:
		print(f"{sys.argv[0]} url_or_domain_list_file")
		exit()
	tld_list=set()
	with open(sys.argv[1]) as f:
		for x in f:
			if x.strip()!="":
				tld = tldextract.extract(x).registered_domain
				if tld!="":
					tld_list.add(tld)
	for x in tld_list:
		print(x)
