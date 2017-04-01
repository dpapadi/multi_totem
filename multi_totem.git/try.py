import urllib2
import json
import ast

def connect(url, cmd, data=None, passwd=None): #from ovxctl ~minor changes~
    try:
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, "admin", passwd)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        req = buildRequest(data, url, cmd)
        ph = opener.open(req)
        j = json.loads(ph.read())
        if 'error' in j:
            print j
            return
        return j['result']
    except urllib2.URLError as e:
        print e
        return
    except urllib2.HTTPError as e:
        if e.code == 401:
            print "Authentication failed: invalid password"
            return
        elif e.code == 504:
            print "HTTP Error 504: Gateway timeout"
            return
        else:
            print e
    except RuntimeError as e:
        print e

def buildRequest(data, url, cmd):   #from ovxctl
    j = { "id" : "ovxctl",  "method" : cmd , "jsonrpc" : "2.0" }
    h = {"Content-Type" : "application/json-rpc"}
    if data is not None:
        j['params'] = data
    return urllib2.Request(url, json.dumps(j), h)


if __name__ == "__main__":
    passwd=""
    req = {"tenantId": 1}
    url = "http://localhost:8080/status"
    result = connect(url, "getVirtualSwitchMapping", data=req, passwd=passwd)  # pass ?
    tmp = ast.literal_eval(json.dumps(result))
    i=1
    for ovx_dpid, map_dict in tmp.iteritems():
        print "try %s" %i
        print "ovx_dpid: " +ovx_dpid
        print "map_dict: " + str(map_dict)
        print
        print
        if len(map_dict["switches"])>1:
            print "big switch"
            for k in map_dict["switches"]:
                if k == "00:00:00:00:00:00:08:00":
                    print ovx_dpid
                    break
            else:
                print "error"
        i+=1
