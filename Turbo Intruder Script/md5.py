# Find more example scripts at https://github.com/PortSwigger/turbo-intruder/blob/master/resources/examples/default.py
import hashlib

def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           requestsPerConnection=100,
                           pipeline=False
                           )

    for i in range(3, 8):
        engine.queue(target.req, randstr(i), learn=1)
#        print(hashlib.md5(str(i).strip()).hexdigest())
        engine.queue(target.req, target.baseInput, learn=2)

    for word in open('/Users/cyal1/github.com/SCRIPT/dictionaries/password/password-8-letter.txt'):
        password = hashlib.md5(word.strip()).hexdigest()
        engine.queue(target.req, password)


def handleResponse(req, interesting):
    if interesting:
        table.add(req)

