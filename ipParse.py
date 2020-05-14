#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:Cyan

"""
Try copying the cluttered IP range contents below to the file and use:
python3 ipParse.py -f filename --smart

192.168.1.0 192.168.2.1/24,192.168.3.4-7,192.168.5.1-.192.168.5.34、192.176.34.6\26、192.187.34.2-67，192.111.111.111，192.168.5.1 - 192.168.5.34 192.168.5.1. -- 0192.168.5.34,192.168.5.1--192.168.5.34、1.2.4.5、192.168.5.5-9
192.168.5.1~192.168.5.34,192.168.5. 1 ~ 192.168.05.0 123.3.3.3. 192.168.5.1~56 192.168.7.1
"""
import re
import argparse
import ipaddress

IPLIST = []
REG_CD = re.compile(
    r'(?P<cd>((([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5]))\.){3})(?P<c1>(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5])))-(?P<c2>(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5])))$')
REG_SUBNET = re.compile(
    r'((([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5]))\.){3}(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5]))\/([0-9]|[1-2][0-9]|3[0-2])$')
REG_IP = re.compile(
    r'((([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5]))\.){3}(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5]))$')
REG_IPRANGE = re.compile(
    r'(?P<bd>((([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5]))\.){2})(?P<c1>(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5])))\.(?P<d1>(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5])))-(?P=bd)(?P<c2>(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5])))\.(?P<d2>(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5])))$')


def replSpace(rep):
    return rep.group().replace(' ', '')


def replPoint(rep):
    return rep.group().strip('.')


def replZero(rep):
    return rep.group().lstrip('0')

# 保存并去重
def save(ip):
    if ip not in IPLIST:
        IPLIST.append(ip)

# 处理 192.168.1.1-192.168.2.128 形式
def ipRange(item):
    res = REG_IPRANGE.match(item)
    bd = res.group('bd')
    c1 = int(res.group('c1'))
    c2 = int(res.group('c2'))
    d1 = int(res.group('d1'))
    d2 = int(res.group('d2'))
    if c1 == c2:
        if d1 < d2:
            for i in range(d1, d2 + 1):
                save(bd + str(c1) + '.' + str(i))
        else:
            print(f'\033[1;31m请检查你的IP:{item}\033[0m')
    elif c1 < c2:
        for c in range(c1, c2 + 1):
            for d in range(d1, 255):
                if c == c2 and d > d2:
                    break
                else:
                    save(bd + str(c) + '.' + str(d))
            d1 = 0
    else:
        print(f'\033[1;31m请检查你的IP:{item}\033[0m')

# 处理 192.168.2.1-243 形式
def dealCd(item):
    res = REG_CD.match(item)
    cd = res.group('cd')
    c1 = int(res.group('c1'))
    c2 = int(res.group('c2'))
    if c1 < c2:
        for i in range(c1, c2 + 1):
            save(cd + str(i))
    else:
        print(f'\033[1;31m请检查你的IP:{item}\033[0m')

# 处理 192.168.1.0/24 形式
def dealSubnet(item):
    if int(re.match(r'.*/(\d+)',item).group(1))<=16:
        print(f'too big range:{item}')
        exit()
    net = ipaddress.ip_network(item, strict=False)
    for ip in net.hosts():
        save(ip)

# 将不同形式的 IP 交给不同的方法处理
def ipParse(iplist):
    for item in iplist:
        # print(item)
        if REG_IPRANGE.match(item):  # 192.168.1.1-192.168.2.128
            ipRange(item)
        elif REG_CD.match(item):  # 192.168.2.1-243
            dealCd(item)
        elif REG_SUBNET.match(item): # 192.168.2.1/24
            dealSubnet(item)
        elif REG_IP.match(item):
            save(item)
        else:
            print(f'\033[1;31m请检查你的IP:{item}\033[0m')

# 处理无格式 IP 范围文件
def smart(ipfile):
    with open(ipfile, encoding="utf-8") as f:
        content = f.read()
    print("-" * 80)
    # 192.168.1.1 -- 254 将不规范的分割符（如： ~~ ~ -- -）全部替换成-,\替换成/
    s1 = re.sub(r'\s*[-~]+\s*', '-', content).replace('\\','/').replace('"','').replace("'",'')
    # 123. 34 .123 . 123 去掉之间多余的空格    -- 如果出错，请注释此行
    s1 = re.sub(r'(\d+\s*\.\s*){3}\d+', replSpace, s1)
    # .123.123.123.123 去掉左右两边误写的.    -- 如果出错，请注释此行
    s1 = re.sub(r'\.?(\d+\.*){3}\d+\.?', replPoint, s1)
    s1 = re.sub(r'\d{2,}', replZero, s1)  # 去掉 123.0.02.1 中 0 开头的多位数
    s1 = re.split(r'[\n\s,，、;；]+', s1) # 以这些符号分隔成列表并去重
    s1 = list({x for x in s1 if x !=''})  
    s1.sort()
    print(s1)
    print("-" * 80)
    ipParse(s1)


def main():
    parser = argparse.ArgumentParser()
    parser.description = 'Parse IP range like 192.168.2.3/26 10.0.4.1-10.0.4.9 10.0.0.1-254'
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", '--file', help="Get IP from the format file")
    group.add_argument("-i", '--iprange', help="-i 192.168.2.3/26,10.0.0.1-254,10.0.4.1-10.0.4.9")
    parser.add_argument('--smart',action="store_true", help="Automatically detect ip from messy files, with '-f'")
    args = parser.parse_args()
    if args.file:
        if args.smart:
            smart(args.file)
        else:
            with open(args.file, encoding="utf-8") as f:
               ip=[i.strip() for i in f if i.strip() !='']
               ip.sort()
               ipParse(ip)       
    elif args.iprange:
        ipParse(args.iprange.strip(',').split(','))
    else:
        print('Use -h to show help')
        exit()
    for i in IPLIST:
        print(i)
    print(f'\033[0;36m共{len(IPLIST)}个IP\033[0m')


if __name__ == '__main__':
    main()
