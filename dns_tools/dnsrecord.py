import dns.resolver
import sys

green = "\x1b[1;32m"
cyan = "\x1b[1;36m"
clear = "\x1b[0m"

record_type = ["A","AAAA","CNAME","NS","MX","TXT","SOA","PTR","AXFR","IXFR",
				"MAILB","URI","HIP","A6","AFSDB","APL","CAA","CDNSKEY","CDS",
				"CSYNC","DHCID","DLV","DNAME","DNSKEY","DS","EUI48","EUI64",
				"MB","MD","MF","MG","MINFO","MR","NAPTR","NINFO","NSAP","NSEC",
				"NSEC3","NSEC3PARAM","NULL","NXT","OPENPGPKEY","OPT","PX","RP",
				"RRSIG","RT","SIG","SPF","SRV","SSHFP","TA","TKEY","TLSA","TSIG",
				"GPOS","HINFO","IPSECKEY","ISDN","KEY","KX","LOC","MAILA",
				"UNSPEC","WKS","X25","CERT","ATMA","DOA","EID","GID","L32",
				"L64","LP","NB","NBSTAT","NID","NIMLOC","NSAP-PTR","RKEY",
				"SINK","SMIMEA","SVCB","TALINK","UID","UINFO","ZONEMD","HTTPS"]

domain = sys.argv[1]

for rt in record_type:
	try:
		r = dns.resolver.resolve(domain, rt)
	except Exception as e:
		print(rt + "\t" + str(e))
		# print(e)
	else:
		# print(rt)
		for v in r:
			print(
				green + rt + clear + "\t" +
				cyan + str(v) + clear)
