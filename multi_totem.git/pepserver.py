from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import pickle
import hashlib
glo_dpid = '1'
key1 = ()
key2 = ()
m = hashlib.md5()

active = {}
expired = {}
mapper = {'inputPort': 'in_port',
          'srcMAC': 'dl_src',
          'dstMAC': 'dl_dst',
          'IPTOS': 'nw_tos',
          'IPProtocol': 'nw_proto',
          'srcIP': 'nw_src',
          'dstIP': 'nw_dst'}


def check():
    print active
    print expired


def check2():
    args = (active,expired,key1,key2)
    b = pickle.dumps(args)
    return b


def return_active():
    pass


def return_expired():
    pass


def construct_hashed_key(match, time_s=None, hash_f=1):
    """
    Depending on the value of hash_f returns different
    hashed objects

    :rtype : hash
    """
    key = (match.dl_src,
           match.dl_dst,
           match.dl_type,
           match.dl_vlan,
           # match.in_port,
           # match.dl_vlan_pcp,
           match.nw_proto,
           match.nw_src,
           match.nw_dst,
           match.nw_tos,
           match.tp_src,
           match.tp_dst,
           time_s)
    print 'printing the values of our soon to be hashed key'
    print key

    if hash_f == 1:

        print hash(key[:len(key) -1])
        return hash(key[:len(key)-1])
    else:
        print hash(key[:len(key) -1])
        return hash(key)


def construct_hashed_sflow(match):
    """

    :param match:
    :return:
    """
    # sfkeys = ['srcMAC', 'dstMAC', 'IPProtocol', 'srcIP', 'dstIP', 'IPTOS']
    # matchkeys = ['dl_vlan', 'tp_src', 'tp_dst']

    # sfkeys = ['srcMAC', 'dstMAC', 'IPProtocol', 'srcIP', 'dstIP', 'IPTOS']
    # matchkeys = ['dl_vlan', 'tp_src', 'tp_dst']
    # vlan propably already sanitized?

    # Adding non existent fields as 'None'
    # print 'bika 72\n'
    # print 'sflow\n',sflow
    # for a in sfkeys:
    #     if a not in sflow:
    #        match[a] = None
    #    else:
    #        if a in ['IPProtocol, IPTOS, tp_src, tp_dst']:
    #            match[a]
    #    print sflow[a]

    # print '76\n'
    # print 'match\n',match
    # for a in matchkeys:
    #     print match[a]
    #     if a not in match:
    #         match[a] = None

    # Converting IPProtocol, IPTOS, tp_src, tp_dst if they are not none

    # Constructing key
    key = (match['dl_src'],
           match['dl_dst'],
           match['dl_type'],
           match['dl_vlan'],
           # match.in_port,
           # match['dl_vlan_pcp'],
           match['nw_proto'],
           match['nw_src'],
           match['nw_dst'],
           match['nw_tos'],
           match['tp_src'],
           match['tp_dst']
           )

    print '97\n'
    key2 = key
    print key
    print hash(key)
    return hash(key)


def construct_dict(match, dpid):
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
    di['dpid'] = dpid
    return di


def construct_new_entry(serialized_match):
    args = pickle.loads(serialized_match)
    match = args[0]
    dpid = args[1]
    time = float(args[2])
    flowmatch = construct_dict(match, dpid)

    # workaround bug 1.2
    # deleting L3 fields from arp
    if match.dl_type == 2054:
        match.nw_src = None
        match.nw_dst = None
        match.nw_proto = None
        match.nw_tos = None
    else:
        match.nw_src = match.nw_src.toStr()
        match.dl_dst = match.nw_dst.toStr()

    print '\n\n___Installing New Entry___'
    d = construct_hashed_key(match)
    print ("Switch: %s,\t Flow(Hash): %s" % (dpid, d))

    # Check if the dpid entry has been initialized
    if dpid not in active:
        active[dpid] = {}

    # Creating the Flow Entry
    # perhaps counterX should be None since if the first packet is sampled it will be 2
    # but in higher sampling rates and for mice flows it might stay zero. Matter of semantics, the flow is registered
    active[dpid][d] = {'counters': {'counterX': 1},
                       'match': flowmatch,
                       'timestamps': {'start': time, 'end': None},
                       }

    # print ('\nActive Bucket\n')
    # print active
    # print ('\nExpired Bucket\n')
    # print expired

    # TODO Return 0,1 and surround with try except
    return pickle.dumps(match)


def move_to_expired(serialized_match):
    args = pickle.loads(serialized_match)
    match = args[0]
    dpid = args[1]
    time = float(args[2])
    e = construct_dict(match, dpid)

    # workaround bug 1.2
    # deleting L3 fields from arp
    if match.dl_type == 2054:
        match.nw_dst = None
        match.nw_src = None
        match.nw_proto = None
        match.nw_tos = None
    else:
        match.nw_src.toStr()
        match.nw_dst.toStr()

    print "\n\n___Moving Expired Entry___"

    e = construct_dict(match, dpid)

    for kk, vv in active[dpid].iteritems():
        print 'now i am parsing:'
        print vv['match']
        if cmp(vv['match'], e) == 0:
            # both work
            # pop() captures and deletes
            # del active[dpid][d]
            found = active[dpid].pop(kk)
            break

    found['timestamps']['end'] = time

    d = construct_hashed_key(match, found['timestamps']['start'], 0)
    print ("Switch: %s,\t Flow(Hash): %s" % (dpid, d))

    if dpid not in expired:
        expired[dpid] = {}

    expired[dpid][d] = found

    # 'if active[dpid]:' does not work
    if active[dpid] == {}:
        del active[dpid]

    # print ("\nActive Bucket\n")
    # print active
    # print ("\nExpired Bucket\n")
    # print expired

    # TODO Return 0,1 and surround with try except
    return pickle.dumps(match)


def collect_sflow(flow):
    # TODO: Need multiple switch support
    # args = pickle.loads(serialized_match)
    # match = args[0]
    # dpid = args[1]
    print '\n\n___Incrementing Counter Entry___'
    sflow = {}
    b = pickle.loads(flow)
    # TODO will try with sflow = b
    for kk, vv in b.iteritems():
        sflow[kk] = vv

    # transition from sflow fields {} to, openflow match {}
    sflowmatch = {}
    # TODO Mechanism for input port??

    # convert dl_type
    dpid = sflow.pop('dpid')
    sflowmatch['dl_type'] = sflow.pop('dl_type')

    # need to check for wildcards?
    if sflow['in_vlan'] == '0':
        sflowmatch['dl_vlan'] = 65535
        del sflow['in_vlan']
    elif sflow['in_vlan'] is not None:
        sflowmatch['dl_vlan'] = int(sflow.pop('in_vlan'))
    else:
        # match['dl_vlan'] = int(sflow['in_vlan'])
        sflowmatch['dl_vlan'] = None

    # unifying UDP/TCP and ICMP or wildcarding
    if 'SrcPort' in sflow:
        # no need to check for Dst Port, since this is a sample and bound to have DST aswell
        sflowmatch['tp_src'] = int(sflow['SrcPort'])
        sflowmatch['tp_dst'] = int(sflow['DstPort'])
    elif 'ICMPType' in sflow:
        sflowmatch['tp_src'] = int(sflow['ICMPType'])
        sflowmatch['tp_dst'] = int(sflow['ICMPCode'])
    else:
        sflowmatch['tp_src'] = None
        sflowmatch['tp_dst'] = None

    fields = ['inputPort', 'srcMAC', 'dstMAC',
              'IPProtocol', 'srcIP', 'dstIP', 'IPTOS']
    # TODO need to add headerbytes
    intfields = ['inputPort', 'IPProtocol', 'IPTOS']

    for a in fields:
        if a not in sflow:
            sflowmatch[mapper[a]] = None
        elif a in intfields:
            sflowmatch[mapper[a]] = int(sflow.pop(a))
        else:
            sflowmatch[mapper[a]] = sflow.pop(a)

    print 'our match should be ready'
    print sflowmatch

    try:
        d = construct_hashed_sflow(sflowmatch)
        # print sflow
        # print match
        # print '227\n'
        print 'Printing Hash: %d\n\n' % d
        print 'Printing of all flows of the DPID: %s' % dpid
        print active[dpid]

        if d in active[dpid]:
            print 'Hash Found'
            active[dpid][d]['counters']['counterX'] += 1
            print active
        else:
            print 'Hash not found'
            for k, v in active[dpid].iteritems():
                for l, w in v['match'].iteritems():
                    if w is None:
                        # TODO possible BUG, maybe implementation specific approach should be check. E.G.
                        # Wildcards means anything (including nothing?? (nothing))
                        # here i assume wild card covers the non existence of wildcards, as POX does
                        # so, we are good and we can continue with next iteration
                        continue
                    elif sflowmatch[l] is None:
                        # (l not in match) or (match[l] is None) was our previous statement. from the way match is
                        # created, seems redundant
                        # key error will not be raised, because if key not present second 'or' will not be evaluated
                        # if we enter here ww, will not be None (wildcards)
                        # so if l is None (not present) difference found
                        break
                    elif sflowmatch[l] == w:
                        # if sample attribute is equal with the match then we have no difference
                        continue
                    else:
                        # if we enter here, there is a difference (should investigate)
                        break
                else:
                    # if loop is completed with no breaks this value under investigation should be incremented
                    active[dpid][k]['counters']['counterX'] += 1
                    # TODO, it should break the outer k, v loop.
                    print 'Flow Reconstructed'
                    break
            else:
                print 'Hash not found, Please accept my apologies'
            # TODO check implemented flow reconstruction, lines 282 - 308
            print 'Hash not Found'
    except:
        print 'Error caught printing match field'
        print sflow
        print sflowmatch
        print 'This should not have happened'

    # TODO: Create functionality to detect wildcards
    # else of a conditional

    # print ("Switch: %s,\t sFlow(Hash): %s" % (dpid, d))
    # print ('\nActive Bucket\n')
    # print active
    # print ('\nExpired Bucket\n')
    # print expired

if __name__ == "__main__":
    # binding server to port
    server = SimpleJSONRPCServer(('localhost', 8080))

    # register functions for usage
    server.register_function(construct_new_entry)
    server.register_function(move_to_expired)
    server.register_function(collect_sflow)
    server.register_function(check)
    server.register_function(check2)

    # start server
    server.serve_forever()
