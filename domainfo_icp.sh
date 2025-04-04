#!/bin/bash

#title：调用免费API接口查询数据
#date: 2022/08/04
#version: v1.3
#update: 优化whois查询返回格式
#update：增加icp备案查询接口

# 备案信息查询接口：https://api.vvhan.com/api/icp?url=www.baidu.com
# ip反查域名接口：api.webscan.cc/?action=query&ip= #暂未调用
# qq信息查询接口：https://api.vvhan.com/api/qq?q
# whois信息查询接口：https://api.devopsclub.cn/api/whoisquery

if [[ ! -n "$1"  ]] ; then #判断变量是否为空,为空则错误
  echo "命令格式错误 示例:./dominfo_free.sh www.test.com"
  else
#请求头和请求URL设置
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
XFF='X-Forwarded-For: 114.114.114.114'
icp_url='https://api.vvhan.com/api/icp?url'
icp2_url='https://api.ooomn.com/api/icp?domain'
whois_url='https://api.devopsclub.cn/api/whoisquery?domain='
qq_url='https://api.vvhan.com/api/qq?qq'

#CURL发起请求
domain_info=`curl -s -m 5 -A "$UA" -H "$XFF" -X GET $icp_url=$1`
icp_info=`curl -s -m 5 -A "$UA" -H "$XFF" -X GET $icp2_url=$1`
whois_info=`curl -s -m 5 -k -A "$UA" -H "$XFF" -X GET $whois_url=$1&type=json&standard=true`
#第一个ICP备案信息获取
domain=`echo $domain_info |jq '.domain' |tr -d '"'`
name=`echo $domain_info |jq '.info.name'|tr -d '"'`
nature=`echo $domain_info |jq '.info.nature' |tr -d '"'`
icp=`echo $domain_info|jq '.info.icp' |tr -d '"'`
title=`echo $domain_info |jq '.info.title' |tr -d '"'`

#第二个ICP备案信息获取
siteindex=`echo $icp_info |jq '.siteindex' |tr -d '"'`
icp_name=`echo $icp_info |jq '.name' |tr -d '"'`
icp_nature=`echo $icp_info |jq '.nature' |tr -d '"'`
icp_icp=`echo $icp_info |jq '.icp' |tr -d '"'`
time=`echo $icp_info |jq '.time' |tr -d '"'`

#第一个whois返回信息截取
registrant=`echo $whois_info | jq '.data.data.registrant' |tr -d '"'`
contactEmail=`echo $whois_info | jq '.data.data.registrantContactEmail' |tr -d '"'`
regtime=`echo $whois_info | jq '.data.data.registrationTime' |tr -d '"'`
exptime=`echo $whois_info | jq '.data.data.expirationTime' |tr -d '"'`
sponsoringRegistrar=`echo $whois_info | jq '.data.data.sponsoringRegistrar' |tr -d '"'`

#第二个whois返回信息截取
status2=`echo $whois_info | jq '.data.status'`
registrar=`echo $whois_info | jq '.data.data.registrar' |tr -d '"'`
registrarAbuseContactEmail=`echo $whois_info | jq '.data.data.registrarAbuseContactEmail' |tr -d '"'`
creationDate=`echo $whois_info | jq '.data.data.creationDate' |tr -d '"'`
registryExpiryDate=`echo $whois_info | jq '.data.data.registryExpiryDate' |tr -d '"'`
registrarAbuseContactPhone=`echo $whois_info | jq '.data.data.registrarAbuseContactPhone' |tr -d '"'`
registrarURL=`echo $whois_info | jq '.data.data.registrarURL' |tr -d '"'`

if [[ "$domain" =~ "null" ]]; then
  echo "----------------------------------------------------------------------------"
  echo "检测域名:"   $siteindex
  echo "备案单位:"   $icp_name
  echo "单位类型:"   $icp_nature
  echo "ICP备案号:"  $icp_icp
  echo "审核通过日期:" $time
else
  echo "----------------------------------------------------------------------------"
  echo "检测域名:"   $domain
  echo "备案单位:"   $name
  echo "单位类型:"   $nature
  echo "ICP备案号:"  $icp
  echo "网站title:"  $title
fi
if [[ "$registrant" =~ "null" ]] && [[ "$status2" == 0 ]]; then
  echo "域名申请单位:" $registrar
  echo "域名注册邮箱:" $registrarAbuseContactEmail
  echo "域名注册电话:" $registrarAbuseContactPhone
  echo "域名注册时间:" $creationDate
  echo "域名到期时间:" $registryExpiryDate
  echo "域名注册平台:" $registrarURL
  echo "----------------------------------------------------------------------------"
else
  echo "域名申请单位:" $registrant
  echo "域名注册邮箱:" $contactEmail
  echo "域名注册时间:" $regtime
  echo "域名到期时间:" $exptime
  echo "域名注册平台:" $sponsoringRegistrar
if [[ "$contactEmail" =~ "qq.com" ]]; then
  qq_id=`echo ${contactEmail%@*}`
  qq_info=`curl -s -m 5 "$UA" -H "$XFF" -X GET $qq_url=$qq_id`
  imgurl=`echo $qq_info | jq '.imgurl' |tr -d '"'`
  qqname=`echo $qq_info | jq '.name' |tr -d '"'`
  echo "qq头像URL:" $imgurl
  echo "qq昵称信息:" $qqname
  fi
  echo "----------------------------------------------------------------------------"
fi
fi

