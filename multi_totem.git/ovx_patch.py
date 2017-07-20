#script with functions necessary for pepserver_stable to work over OpenVirteX

import urllib2
import json
import ast

def confirm_tenant(tid, passwd):
    return True

def bsw_address_mapping (url, ten_ip, ten_id, mac, passwd=""):
    req = {"tenantId": ten_id}
    url = url % "status"
    result = connect(url, "getVirtualHosts", data=req, passwd=passwd)
    tmp = ast.literal_eval(json.dumps(result))
    for k in tmp:
        if 'ipAddress' in k.keys() and k["mac"] == mac:
            ip = k["ipAddress"]
            break
    else:
        return "NONE"
    print "For physical ip: " + ten_ip + " from tenant network: %s" % ten_id
    print "mac --> " + mac
    print "ip  --> " + ip
    return ip

def address_mapping(url, ten_ip, ten_id, passwd=""):
    req = {}
    url = url % "status"
    result = connect(url, "getPhysicalHosts", data=req, passwd=passwd) #pass ?
    tmp = ast.literal_eval(json.dumps(result))
    for k in tmp:
        if 'ipAddress' in k.keys() and k["ipAddress"] == ten_ip:
            mac = k["mac"]
            break
    else:
        req = {"tenantId": ten_id}
        result = connect(url, "getVirtualHosts", data=req, passwd=passwd)
        tmp = ast.literal_eval(json.dumps(result))
        for k in tmp:
            if 'ipAddress' in k.keys() and k["ipAddress"] == ten_ip:
                mac = k["mac"]
                break
        else:
            return ("NONE", "NONE", False)
        print "MAC reparation successfull!"
        print "Tenant ID:      %s" % ten_id
        print "IP       :     " + ten_ip
        print "MAC(repaired): " + mac
        return (mac, ten_ip, True)
    req = {"tenantId": ten_id}
    result = connect(url, "getVirtualHosts", data=req, passwd=passwd)
    tmp = ast.literal_eval(json.dumps(result))
    for k in tmp:
        if 'ipAddress' in k.keys() and k["mac"] == mac:
            ip = k["ipAddress"]
            break
    else:
        return ("NONE", "NONE", False)
    print "For physical ip: " + ten_ip + " from tenant network: %s" % ten_id
    print "mac --> " + mac
    print "ip  --> " + ip
    return (mac, ip, False)

def dpid_mapping(url, dpid, ten_id, passwd=""):
    is_bsw = False
    req = {"tenantId": ten_id}
    url = url % "status"
    result = connect(url, "getVirtualSwitchMapping", data=req, passwd=passwd)  # pass ?
    tmp = ast.literal_eval(json.dumps(result))
    for ovx_dpid, map_dict in tmp.iteritems():
        if len(map_dict["switches"])>1:
            print "big switch"  # temp
            is_bsw = True
        for k in map_dict["switches"]:
            if k == dpid:
                return is_bsw,ovx_dpid
    else:
        print "No dpid mapping for dpid: " + dpid + "from tenant id: " +ten_id
        return is_bsw, "NONE"

def mod_dpid(dpid):
    mod_dpid = ""
    for k in range(0, len(dpid), 2):  # modify the dpid to 00:a4:23:05:00:00:00:xx
        if k == 0:
            mod_dpid += "00:"
        else:
            mod_dpid += ":"
        mod_dpid += dpid[k]
        mod_dpid += dpid[k + 1]
    return mod_dpid

def get_tid(url, mac, passwd=""):
    req = {}
    url = url % "status"
    result = connect(url, "getPhysicalHosts", data=req, passwd=passwd) #pass ?
    tmp = ast.literal_eval(json.dumps(result))
    for k in tmp:
        if 'ipAddress' in k.keys() and k['mac'] == mac:
            i = 0
            tid = ""
            while True:
                tid += k['ipAddress'][i]
                i += 1
                if k['ipAddress'][i] == '.':
                    return tid
                if i > 3:
                    print "Error in while loop from function get_tid!"
                    break
    return "NONE"



#functions from ovxctl to 'talk' to OVX server

def connect(url, cmd, data=None, passwd=None): #from ovxctl ~minor changes~ tid=None(??)
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