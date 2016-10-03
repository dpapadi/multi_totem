def confirm_tenant():
    return True

def address_mapping(url, ten_ip, ten_id, pass=""):
    req = {}
    url = url % "status"
    result = connect(url, "getPhysicalHosts", data=req) #pass ?
    tmp = json.dumps(result)







    def address_mapping(ten_ip, ten_id):  # ten_id --> tenant id (example 1)
        # port=[]
        os.chdir(HYP_DIR)  # ten_ip --> IP to be de-virtualized
        commands = []
            # ten_id = ten_ip[0]  # works for 1-9 tenants
            commands.append("python ovxctl.py -n getPhysicalHosts\n")
            commands.append("python ovxctl.py -n getVirtualHosts %s\n" % ten_id)
            tmp = ast.literal_eval(os.popen(commands[0]).read())
            try:
                for k in tmp:
                    if 'ipAddress' in k.keys() and k["ipAddress"] == ten_ip:
                        mac = k["mac"]
                        break
                else:
                    tmp = ast.literal_eval(os.popen(commands[1]).read())
                    for k in tmp:
                        if 'ipAddress' in k.keys() and k["ipAddress"] == ten_ip:
                            mac = k["mac"]
                            # port=int(k["port"])
                            break
                    else:
                        return ("NONE", "NONE")
                    print
                    "MAC reparation successfull!"
                    print
                    "Tenant ID:     " + ten_id
                    print
                    "IP       :     " + ten_ip
                    print
                    "MAC(repaired): " + mac
                    return (mac, ten_ip)
                tmp = ast.literal_eval(os.popen(commands[1]).read())
                for k in tmp:
                    if 'ipAddress' in k.keys() and k["mac"] == mac:
                        ip = k["ipAddress"]
                        # port=int(k["port"])
                        break
                print
                "For physical ip: " + ten_ip + " from tenant network: " + ten_id
                print
                "\nmac --> " + mac
                print
                "ip  --> " + ip
                return (mac, ip)
            except:
                print
                "Error in address_mapping function!\n"
                return ("NONE", "NONE")


def dpid_mapping():
    def dpid_mapping(dpid, mac):
        os.chdir(HYP_DIR)
        commands = []
        commands.append("python ovxctl.py -n getPhysicalHosts\n")
        tmp = ast.literal_eval(os.popen(commands[0]).read())
        try:
            for k in tmp:  # find the tenant id of the flow
                if 'ipAddress' in k.keys() and k["mac"] == mac:
                    tid = k["ipAddress"][0]
                    break
            else:
                return dpid
            commands.append("python ovxctl.py -n getVirtualSwitchMapping %s\n" % tid)
            mod_dpid = ""
            for k in range(0, len(dpid), 2):  # modify the dpid to 00:a4:23:05:00:00:00:xx
                if k == 0:
                    mod_dpid += "00:"
                else:
                    mod_dpid += ":"
                mod_dpid += dpid[k]
                mod_dpid += dpid[k + 1]
            tmp = ast.literal_eval(
                os.popen(commands[1]).read())  # find the dpid throught the VirtualSwitchMapping of ovxctl
            new_dpid = tmp[mod_dpid]['switches']
            return new_dpid[0]
        except Exception:
            print
            "Error in dpid_mapping function"
            return dpid

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