#! /bin/zsh

function curl_wapper(){
	curl -k -s -o /dev/null -m 1 --path-as-is -w "%{http_code}","%{size_download}" -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36" "$@"
}

cat $1|while read line; do
	echo "\e[1m\e[32m$line\e[0m"
	curl_wapper -H "X-Forwarded-Host: $2" "$line"; echo "\t\t=> X-Forwarded-Host: $2" &
	curl_wapper -H "X-Forwarded-For: $2" "$line"; echo "\t\t=> X-Forwarded-For: $2" &
	curl_wapper -H "X-Host: $2" "$line"; echo "\t\t=> X-Host: $2" &
	curl_wapper -H "Host: $2" "$line"; echo "\t\t=> Host: $2"
done