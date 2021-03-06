#!/usr/bin/python

from timeout import timeout
from timeout import TimeoutError
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import pickle
from kafka.client import KafkaClient
from kafka.consumer import KafkaConsumer
import hashlib
from struct import unpack
from socket import inet_aton
import ovx_patch
import sys
import time

# 2 counters to calculate the "sample with no info" effect
swni_cntr = 0  #counts the times a sample with no info is collected
sflow_cntr = 0 #counts the number collect_sflow is used

#boolean for OVX
OVX_enable = False

# Global Dictionaries

#hypervisor dictionary
hypervisor_var = {}

# Active Flows
active = {}

# Expired Flows
expired = {}

# Used as a MAC Table, matching OF ports to MAC addresses
mac_table = {}

# big switches
big_switches = {}

# Structure to match sflow fields to OpenFlow fields
mapper = {'inputPort': 'in_port',
          'srcMAC': 'dl_src',
          'dstMAC': 'dl_dst',
          'IPTOS': 'nw_tos',
          'IPProtocol': 'nw_proto',
          'srcIP': 'nw_src',
          'dstIP': 'nw_dst'}


def construct_hashed_key(match, time_s=None, hash_f=1):
    """
	:params (OpenFlow match, timestamp, flag)
	Depending on the value of hash_f returns different
    hashed objects
    :rtype : hashed value
    """
    key = (match.in_port,
           match.dl_src.toStr(),
           match.dl_dst.toStr(),
           match.dl_type,
           match.dl_vlan,
           # match.dl_vlan_pcp,
           match.nw_proto,
           match.nw_src.toStr(),
           match.nw_dst.toStr(),
           match.nw_tos,
           match.tp_src,
           match.tp_dst,
           time_s)
    # print 'printing the values of our soon to be hashed key'
    # print key

    if hash_f == 1:
        #if hash_f == 1, don't include the timestamp parameter
        print hash(key[:len(key) -1])
        return hash(key[:len(key)-1])
    else:
        # else include it
        print hash(key[:len(key) -1])
        return hash(key)


def construct_hashed_sflow(match):
    """
    :param match: OpenFlow match object
    :return: hashed value
    """
    # Constructing key
    key = (match['in_port'],
           match['dl_src'],
           match['dl_dst'],
           match['dl_type'],
           match['dl_vlan'],
           # match['dl_vlan_pcp'],
           match['nw_proto'],
           match['nw_src'],
           match['nw_dst'],
           match['nw_tos'],
           match['tp_src'],
           match['tp_dst']
           )

    # print key
    print hash(key)
    return hash(key)

def construct_dict(match, dpid):
    """
    :param match: OpenFlow match object, dpid
    :return: dictionary with those values
    """
    di = {}
    di['in_port'] = match.in_port
    di['dl_src'] = match.dl_src.toStr()
    di['dl_dst'] = match.dl_dst.toStr()
    di['dl_type'] = match.dl_type
    di['dl_vlan'] = match.dl_vlan
    # di['dl_vlan_pcp'] = match.dl_vlan_pcp
    di['nw_proto'] = match.nw_proto
    di['nw_src'] = match.nw_src.toStr()
    di['nw_dst'] = match.nw_dst.toStr()
    di['nw_tos'] = match.nw_tos
    di['tp_src'] = match.tp_src
    di['tp_dst'] = match.tp_dst
    #di['dpid'] = dpid no need, matches sorted by tid, dpid
    return di


def construct_new_entry(args):
    """
    :param match: serialized OpenFlow match
    """
    #args = pickle.loads(serialized_match)
    match = args[0]
    #print construct_dict(match, None)
    #raw_input() #temp

    if OVX_enable:
        tid = int(args[3])  # get the tid and passwd from the controller
        dpid = hex(int(args[1]))  # converts the decimal of the dpid to the actual value
        dpid = ovx_patch.mod_dpid(dpid[2:])
        passwd = args[4]
        if tid not in big_switches:
            big_switches[tid] = []
        if dpid not in big_switches[tid] and ovx_patch.discover_bsw(hypervisor_var['url'], dpid, tid, passwd):
            big_switches[tid].append(dpid)
            print "\nbig switches : \n"
            print big_switches # temp
            print
            print
        if tid not in hypervisor_var['tenants']:
            hypervisor_var['tenants'][tid] = {'dpid': {}, 'ip': {'IP': {}, 'MAC': {}}}
        if not ovx_patch.confirm_tenant(tid, passwd):
            print "Tenant Id confirmation failed. Id: %s" % tid
            return
    else:
        dpid = hex(int(args[1]))[2:]
        tid = 0

    print "mod_dpid "+dpid #temp

    time = float(args[2])
    # print '\n\n___Installing New Entry___'
    #match_dict = construct_dict(match, dpid)

    # Construct hashed value based on match
    d = construct_hashed_key(match)

    # print ("Switch: %s,\t Flow(Hash): %s" % (dpid, d))

    # Check if the dpid entry has been initialized
    if tid not in active:
        active[tid] = {}
    if dpid not in active[tid]:
        active[tid][dpid] = {}

    # Creating the Flow Entry
	# if the flow rule is not already in the Active structure
    if d not in active[tid][dpid]:
        active[tid][dpid][d] = {'counters': {'counterX': 1, 'Packet_In': 1, 'mult_Packet_in': 1},
                           'match': construct_dict(match, dpid),
                           'timestamps': {'start': time, 'end': None},
                           'headers': {},
                           'physicalDPID': None,
                           'tenant': tid
                           }
        hlp = active[tid][dpid][d]['match']
        # assign the flow entry to a flowspace
        # assign_flowspace(d, dpid)
	# else increment a counter measuring multiple packetIns
    else:
        active[tid][dpid][d]['counters']['mult_Packet_in'] += 1
        hlp = active[tid][dpid][d]['match']

    # MAC Table
    if tid not in mac_table:
        mac_table[tid] = {}
    if dpid not in mac_table[tid]:
        mac_table[tid][dpid] = {}
        mac_table[tid][dpid][hlp['dl_src']] = hlp['in_port']
    else:
        mac_table[tid][dpid][hlp['dl_src']] = hlp['in_port']


    #print mac_table

    # assign_flowspace(d, dpid)


def move_to_expired(args, scnd=False):
    """
    :param match: serialized OpenFlow match
    :return:
    """
    #args = pickle.loads(serialized_match)
    match = args[0]
    if OVX_enable:
        tid = int(args[3])  # get the tid and passwd from the controller
        dpid = hex(int(args[1]))  # converts the decimal of the dpid to the actual value
        dpid = ovx_patch.mod_dpid(dpid[2:])
    else:
        dpid = hex(int(args[1]))[2:]
        tid = 0
    passwd = args[4]
    if not ovx_patch.confirm_tenant(tid, passwd):
        print "Tenant Id confirmation failed. Id: %s" % tid
        return
    time = float(args[2])
    # print "\n\n___Moving Expired Entry___"

	# create a hash value for the expired flow (not including timestamp)
    e = construct_hashed_key(match)

    #while True:
    try:
    # if there is such a flow
        if e in active[tid][dpid]:
            # remove the flow
            found = active[tid][dpid].pop(e)
            found['timestamps']['end'] = time

            # now create another hashed value, including timestamp
            d = construct_hashed_key(match, found['timestamps']['start'], 0)

            if tid not in expired:
                expired[tid] = {}
            if dpid not in expired[tid]:
                expired[tid][dpid] = {}

            expired[tid][dpid][d] = found
            print "move_to_expired function!" #temp
            try:
                if active[tid][dpid] == {}:
                    del active[tid][dpid]
                    print "active entry (dpid) deleted!" #temp
                if active[tid] == {}:
                    del active[tid]
                    print "active entry (tid) deleted" #temp
                return
            except:
                print "error in small try of move to expired!"
                return
        else:
            print " ..Move to expired.. else section."
            if not scnd:
                if match.nw_tos == 0 and match.tp_src == 0 and match.tp_dst == 0:
                    match.nw_tos = None
                    match.tp_src = None
                    match.tp_dst = None
                    args = (match, args[1], args[2], args[3], args[4])
                    move_to_expired(args, True)
                    return
            else:
                print "Move to Expired FAILED!!!!"
                return
    except Exception as ex:
        print ex
        print "error in wide try of move to expired!"
        return


def collect_sflow(flow):
    """
    :param match: serialized sflow sample
    :return:
    """
    global sflow_cntr
    sflow_cntr += 1
    # print '\n\n___Incrementing Counter Entry___'
    sflow = {}

    #b = pickle.loads(flow)

    # TODO will try with sflow = b
    for kk, vv in flow.iteritems():
        sflow[kk] = vv

    # transition from sflow fields {} to, openflow match {}
    match = {}

    # convert dl_type
    match['dl_type'] = sflow.pop('dl_type')
    sflow_dpid = sflow.pop('dpid')
    #procedure for hypervisor (OVX) mode
    if OVX_enable:
        try:
            if 'srcIP' not in sflow.keys():
                print "Sample with no info" #sample due to OpenVirteX internal signals (?)
                global swni_cntr
                swni_cntr += 1
                return
            else:
                if sflow['dstMAC'] == 'ff:ff:ff:ff:ff:ff':
                    print 'Ignoring broadcast messages...'
                    return
                if sflow['srcMAC'][:8] == 'a4:23:05':
                    tid = int(sflow['srcMAC'][10:11])

                    if sflow_dpid not in hypervisor_var['tenants'][tid]['dpid']:
                        (is_bsw, dpid) = ovx_patch.dpid_mapping(hypervisor_var['url'], sflow_dpid, tid, passwd="")
                        if dpid == "NONE":
                            return
                        hypervisor_var['tenants'][tid]['dpid'][sflow_dpid] = (is_bsw, dpid)
                    else:
                        dpid = hypervisor_var['tenants'][tid]['dpid'][sflow_dpid][1]

                    tmp = sflow['srcIP'] #debug issue
                    sflow_ip = sflow['srcIP']
                    if sflow_ip not in hypervisor_var['tenants'][tid]['ip']:
                        (sflow['srcMAC'], sflow['srcIP'], rep_mac) = ovx_patch.address_mapping(hypervisor_var['url'], sflow['srcIP'], tid, passwd="")
                        if sflow['srcIP'] == "NONE":
                            print "No mapping found for srcIP"
                            return
                        if not rep_mac:
                            hypervisor_var['tenants'][tid]['ip'][sflow_ip] = {}
                            hypervisor_var['tenants'][tid]['ip'][sflow_ip]['IP'] = sflow['srcIP']
                            hypervisor_var['tenants'][tid]['ip'][sflow_ip]['MAC'] = sflow['srcMAC']
                    else:
                        sflow['srcIP'] = hypervisor_var['tenants'][tid]['ip'][sflow_ip]['IP']
                        sflow['srcMAC'] = hypervisor_var['tenants'][tid]['ip'][sflow_ip]['MAC']

                    sflow_ip = sflow['dstIP']
                    if sflow_ip not in hypervisor_var['tenants'][tid]['ip']:
                        (sflow['dstMAC'], sflow['dstIP'], rep_mac) = ovx_patch.address_mapping(hypervisor_var['url'], sflow['dstIP'], tid, passwd="")
                        if sflow['dstIP'] == "NONE":
                            print "No mapping found for dstIP"
                            return
                        if not rep_mac:
                            hypervisor_var['tenants'][tid]['ip'][sflow_ip] = {}
                            hypervisor_var['tenants'][tid]['ip'][sflow_ip]['IP'] = sflow['dstIP']
                            hypervisor_var['tenants'][tid]['ip'][sflow_ip]['MAC'] = sflow['dstMAC']
                    else:
                        sflow['dstIP'] = hypervisor_var['tenants'][tid]['ip'][sflow_ip]['IP']
                        sflow['dstMAC'] = hypervisor_var['tenants'][tid]['ip'][sflow_ip]['MAC']
                else:
                    tid = int(ovx_patch.get_tid(hypervisor_var['url'], sflow['srcMAC'], passwd=""))
                    (is_bsw, dpid) = ovx_patch.dpid_mapping(hypervisor_var['url'], sflow_dpid, tid, passwd="")
                    if is_bsw:
                        swni_cntr += 1
                        return   #ignore samples from the core switdhes of the bsw
                        tmp = sflow['srcIP']  # debug issue
                        sflow_ip = sflow['srcIP']
                        if sflow_ip not in hypervisor_var['tenants'][tid]['ip']:
                            sflow['srcIP'] = ovx_patch.bsw_address_mapping(hypervisor_var['url'], sflow['srcIP'], tid, sflow['srcMAC'], passwd="")
                            if sflow['srcIP'] == "NONE":
                                print "No mapping found for srcIP"
                                return
                            hypervisor_var['tenants'][tid]['ip'][sflow_ip] = {}
                            hypervisor_var['tenants'][tid]['ip'][sflow_ip]['IP'] = sflow['srcIP']
                            hypervisor_var['tenants'][tid]['ip'][sflow_ip]['MAC'] = sflow['srcMAC']
                        else:
                            sflow['srcIP'] = hypervisor_var['tenants'][tid]['ip'][sflow_ip]['IP']
                            sflow['srcMAC'] = hypervisor_var['tenants'][tid]['ip'][sflow_ip]['MAC']


                        sflow_ip = sflow['dstIP']
                        if sflow_ip not in hypervisor_var['tenants'][tid]['ip']:
                            sflow['dstIP'] = ovx_patch.bsw_address_mapping(hypervisor_var['url'], sflow['dstIP'], tid, sflow['dstMAC'], passwd="")
                            if sflow['dstIP'] == "NONE":
                                print "No mapping found for dstIP"
                                return
                            hypervisor_var['tenants'][tid]['ip'][sflow_ip] = {}
                            hypervisor_var['tenants'][tid]['ip'][sflow_ip]['IP'] = sflow['dstIP']
                            hypervisor_var['tenants'][tid]['ip'][sflow_ip]['MAC'] = sflow['dstMAC']
                        else:
                            sflow['dstIP'] = hypervisor_var['tenants'][tid]['ip'][sflow_ip]['IP']
                            sflow['dstMAC'] = hypervisor_var['tenants'][tid]['ip'][sflow_ip]['MAC']
        except Exception as e:
            print e
            print "error in collect_sflow first try section"
            return
    else:
        try:
            tid=0
            dpid=sflow_dpid
        except:
            return
    # manipulate VLAN tag
    if sflow['in_vlan'] == '0':
        match['dl_vlan'] = 65535
        del sflow['in_vlan']
    elif sflow['in_vlan'] is not None:
        match['dl_vlan'] = int(sflow.pop('in_vlan'))
    else:
        match['dl_vlan'] = None

    # unifying UDP/TCP/ICMP or wildcarding
    if 'SrcPort' in sflow:
        # no need to check for Dst Port, since this is a sample and bound to have DST aswell
        match['tp_src'] = int(sflow['SrcPort'])
        match['tp_dst'] = int(sflow['DstPort'])
    elif 'ICMPType' in sflow:
        match['tp_src'] = int(sflow['ICMPType'])
        match['tp_dst'] = int(sflow['ICMPCode'])
    else:
        match['tp_src'] = None
        match['tp_dst'] = None
        #raw_input("None tp_src in sflow sample!!")

    fields = ['inputPort', 'srcMAC', 'dstMAC',
              'IPProtocol', 'srcIP', 'dstIP', 'IPTOS']

    intfields = ['inputPort', 'IPProtocol', 'IPTOS']

    # translate rest of the fields using the structure mapper{}
    for a in fields:
        if a not in sflow:
            match[mapper[a]] = None
        elif a in intfields:
            match[mapper[a]] = int(sflow.pop(a))
        else:
            match[mapper[a]] = sflow.pop(a)

    try:
        match['in_port'] = mac_table[tid][dpid][match['dl_src']]
    except Exception as g:
        print 'hi ' + str(g)
        match['in_port'] = 0

    # print 'OpenFlow Match:'
    # print match
    try:
        d = construct_hashed_sflow(match)

        print 'Printing Hash: %d\n' % d
        if d in active[tid][dpid]:
            print 'Hash Found'
            active[tid][dpid][d]['counters']['counterX'] += 1
            active[tid][dpid][d]['physicalDPID'] = sflow_dpid #maybe temp
            # adding headers of packet

            # f = match['headerBytes']
            # e = hash(f)
            # if e not in active[dpid][d]['headers']:
            #    active[dpid][d]['headers'][e] = f

            # print active
        else:
            # print 'Printing of all flows of the DPID: %s' % dpid
            print'this active: '
            print active[tid][dpid]
            try:
                print tmp
            except:
                print 'No need!'
            print 'Hash not found'
            print "\n match: "
            print match
            print
            print
            print
            print
            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            # same functionality as in assign_flowspace()
            for kk, vv in active[tid][dpid].iteritems():
                for ll, ww in vv['match'].iteritems():
                    if ww is None:
                        # can continue with next iteration
                        continue
                    elif (ll not in match) or (match[ll] is None):
                        # key error will not be raised, because if key not present second 'or' will not be evaluated
                        break
                    elif match[ll] == ww:
                        # if sample attribute is equal with the match then we have no difference
                        continue
                    else:
                        if (ll == 'nw_src') or (ll == 'nw_dst'):
                            # special support for ip
                            frl = ww.split('/')
                            if len(frl) == 1:
                                # A.B.C.D
                                # should have been caught by outer elif
                                break

                            # A.B.C.D/M
                            tmp = int(frl[1])
                            frl_mask = int((tmp * '1' + (32 - tmp) * '0'), 2)
                            # sflow: a.b.c.d
                            if (unpack("!L", inet_aton(match[ll]))[0] & frl_mask) == unpack("!L", inet_aton(frl[0]))[0]:
                                continue
                            else:
                                break
                        else:
                            # not same value, (or something else)
                            # print '4'
                            break
                else:
                    # if loop is completed with no breaks this value under investigation should be incremented
                    active[tid][dpid][kk]['counters']['counterX'] += 1
                    active[tid][dpid][d]['physicalDPID'] = sflow_dpid  # maybe temp
                    print 'Flow Reconstructed'
                    break
            else:
                print 'Hash Reconstrution failed.\n'
                print "dpid" + dpid
                print "sflow_dpid" + sflow_dpid
    except Exception as sd:
        print 'bad dpid ' + dpid
        print sd
        print 'Error caught.\nPrinting match field'
        print sflow
        print match
        print 'This should not have happened'
    # print ("Switch: %s,\t sFlow(Hash): %s" % (dpid, d))


def get_input_from_queue(serialized_request):
    args = pickle.loads(serialized_request)
    #print args
    func = args[0]
    if len(args) > 2:
        func += "(args[1:])"
    else:
        func += "(args[1])"
    #try:temp
    exec(func)
    #except:
     #   print "Error with serialized request!"
        # return
    print "Correct input from queue!" #temp
    return

def register_queue():
    tryagain = True
    while tryagain:
        while tryagain:#temp
        #try:
            #kafka = KafkaClient('localhost:9092')
            global main_consumer  # consumer for kafka queue
            global client_consumer
            main_consumer = KafkaConsumer("main", group_id="gid", bootstrap_servers='localhost:9092', consumer_timeout_ms=0, max_poll_records=1)
            client_consumer = KafkaConsumer("client", group_id="gid2", bootstrap_servers='localhost:9092',consumer_timeout_ms=0)
            tryagain = False
            print "Queuing system is up."
        #except Exception:
         #   print "Queuing system not ready yet."
          #  time.sleep(5)
    return


@timeout(3)
def handle_request():
    try:
        server.handle_request()
    except TimeoutError:
        print "Timeout Error in handle request.\n\n"
        return

def checkout():
    """
    :params None
    :rtype : Serialized tuple containing active and expired dictionaries
    """
    args = (active, expired)
    b = pickle.dumps(args)
    return b
    #tmp = "Successfull Attempt"
    #args = (tmp, False)
    #b = pickle.dumps(args)
    #print tmp
    #return b

def get_samplewithnoinforate():
    try:
        rate = swni_cntr / (1.0 * sflow_cntr)
        msg = "We collected %s samples with no info out of %s sflow samples.\nPercentage: %.2f" % (swni_cntr, sflow_cntr, rate)
        return msg
    except:
        return "Something went wrong with the data collected.\n\n"

if __name__ == "__main__":
    a = len(sys.argv)
    if a == 2:          #input for configuring a hypervisor
        print "Running in Hypervisor mode."
        file_name = sys.argv[1]
        try:
            with open(file_name) as f:
                for line in f:
                    (key, val) = line.split()
                    hypervisor_var[key] = val
        except IOError:
            print "No such file: \t%s\n" % file_name
            exit()
    else:
        print "Running in Normal mode."
    register_queue()

    if 'name' in hypervisor_var.keys() and hypervisor_var['name']=='OpenVirteX':
        hypervisor_var['tenants']={}
        OVX_enable=True
    if a == 2:
        print hypervisor_var

    # binding server to port
    server = SimpleJSONRPCServer(('localhost', 8085))

    # register functions for usage
    server.register_function(checkout)
    server.register_function(get_samplewithnoinforate)

    # serve_forever
    msg_cnt=0
    while True:
        while True:
        #try:temp
            cl_req = client_consumer.poll()
            if bool(cl_req):
                #print "handle request"
                handle_request()
            msg = main_consumer.poll()
            if bool(msg):
                i = len(str(msg.values()).split()[6])-1
                #print eval(str(msg.values()).split()[6][6:i])
                get_input_from_queue(eval(str(msg.values()).split()[6][6:i]))
        #except Exception:
         #   msg_cnt += 1
          #  print "Error n%s" % msg_cnt

