import time, json, os, requests, urllib2

CONFIG_FILE = 'config.json'

"""
Open and load a file at the json format
"""

def open_and_load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            return json.loads(config_file.read())
    else:
        print "File [%s] doesn't exist, aborting." % (CONFIG_FILE)
        sys.exit(1)

def print_event(r):
    print r['id'] + ": " + r['dt'] + " [" + r['user'] + " (" + r['login'] +")] " + r['source']

"""
Main
"""

if __name__ == "__main__":
    config = open_and_load_config()
    url = config['url']
    tmp = urllib2.urlopen(url).read()
    res = json.loads(tmp)[0]
    last_id = res['id']
    print_event(res)
    while 1:
        try:
            url = config['url'] + "?id=" + last_id
            tmp = urllib2.urlopen(url).read()
            if (tmp != "null"):
                res = json.loads("["+ tmp + "]")
                for re in res:
                    for id, r in re.items():
                        if (r['id'] != last_id):
                            if (r['login'] != ""):
                                print_event(r)
                            last_id = r['id']
        except Exception as e:
            print "EXCEPTION: "
            print e
            pass
        time.sleep(1)
