#!/usr/bin/python

from timeout import timeout
from timeout import TimeoutError
import sys
import pickle
import csv
import time
import jsonrpclib
from kafka.client import KafkaClient
from kafka.producer import KafkaProducer

server = jsonrpclib.Server('http://localhost:8085')

# Active/Expired Flows
active = {}
expired = {}

def construct_hashed_sflow(match):
    """
    :params: OpenFlow match object
    :return: hashed value computed on that object
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

    return hash(key)

def register_queue():
    tryagain = True
    while tryagain:
        try:
            kafka = KafkaClient(bootstrap_servers="localhost:9092")
            global producer
            producer = KafkaProducer(bootstrap_servers="localhost:9092")
            tryagain = False
        except Exception:
            print "Kafka is unavailable at the moment."
            time.sleep(5)
    return

@timeout(5)
def checkout():
    try:
        a=server.checkout()
        return a
    except TimeoutError:
        print "Timeout Error in checkout() function"
        return 0

def update_data():
    activate_server()
    #time.sleep(0.5)
    a=checkout()
    if a:
        args = pickle.loads(a)
        global table
        table = args
        print "Data updated"
        print "\n\n"
        return table
    else:
        update_data()

def activate_server():
    try:
        producer.send("client", "hi")
    except:
        print "Error in queue!"
        register_queue()
        return
    return

def ret_active():
    #while True:
    try:
        tid = raw_input("Enter Tenant ID (0 for all tenant counters) or r to return: ")
        if tid == "r":
            return
        elif int(tid) == 0:
            print "\nactive: "
            print table[0]
            return
        else:
            print "\nactive: "
            print table[0][int(tid)]
        print "\n\n"
        opt = raw_input("Write active counters to csv format(Y/N) ?  ")
        if opt == "Y" or opt == "y":
            output(int(tid), 1)
    except Exception:
        print "\n\nSomething went wrong. Please enter a valid option.\n\n"
        ret_active()
    return

def ret_expired():
    try:
        tid = raw_input("\nEnter Tenant ID (0 for all tenant counters) or r to return: ")
        if tid == "r":
            return
        elif int(tid) == 0:
            print table[1]
            print "\nexpired: "
        else:
            print "\nexpired: "
            print table[1][int(tid)]
        print "\n\n"
        opt = raw_input("Write expired counters to csv format(Y/N) ?  ")
        if opt == "Y" or opt == "y":
            output(int(tid), 1)
    except Exception:
        print "\n\nSomething went wrong. Please enter a valid option.\n\n"
        ret_expired()
    return

def output(tid, t, start=0, end=float("inf")):
    name = raw_input("\n\nPlease Enter a file name to print flows to:\t")
    filename = '%s.csv' %name
    with open(filename, 'w') as csvfile:
        fieldnames = ['dpid', 'hash', 'in_port', 'dl_src', 'dl_dst', 'dl_type', 'dl_vlan', 'nw_proto', 'nw_src',
                      'nw_dst', 'nw_tos', 'tp_src', 'tp_dst', 'Packet_Counter', 'Packet_In','tenant', 'physicalDPID']

        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        temp=table[t]
        for ten_id, fr in temp.iteritems() :
            if tid == 0 or ten_id == tid :
                for kk, vv in fr.iteritems():
                    for l, w in vv.iteritems():
                        if w['timestamps']['start'] > start and w['timestamps']['end'] < end:
                            b = w['match']
                            b['dpid'] = kk
                            b['hash'] = l
                            b['Packet_Counter'] = w['counters']['counterX']
                            b['Packet_In'] = w['counters']['Packet_In']
                            b['tenant'] = w['tenant']
                            b['physicalDPID'] = w['physicalDPID']
                            writer.writerow(b)
    print '\n\nOutput Successfull!\n\n'
    return

def aggregate():
    try:
        tid = raw_input("\nEnter Tenant ID (0 for all tenant counters) or r to return: ")
        if tid == 'r':
            return
        tid = int(tid)
    except:
        print "\n\nSomething went wrong. Please enter a valid option.\n\n"
        aggregate()
    print '\n\nPrinting Aggregate Counters\n\n'
    aggr = table[0]
    temp = table[1]
    for ten_id, fr in temp.iteritems():
        if tid == 0 or ten_id == tid:
            for dpid, rest in fr.iteritems():
                for hashes, dicts in rest.iteritems():
                    hk = construct_hashed_sflow(dicts['match'])
                    print 'Hash Key: %s' % hk
                    if ten_id not in aggr:
                        aggr[ten_id] = {}
                    if dpid not in aggr[ten_id]:
                        aggr[ten_id][dpid] = {}
                        aggr[ten_id][dpid][hk] = dicts
                        aggr[ten_id][dpid][hk]['counters']['Packet_In'] = 1
                    elif hk not in aggr[ten_id][dpid]:
                        aggr[ten_id][dpid][hk] = dicts
                        aggr[ten_id][dpid][hk]['counters']['Packet_In'] = 1
                    else:
                        aggr[ten_id][dpid][hk]['counters']['counterX'] += dicts['counters']['counterX']
                        try:
                            aggr[ten_id][dpid][hk]['counters']['Packet_In'] += 1
                        except KeyError:
                            aggr[ten_id][dpid][hk]['counters']['Packet_In'] = 1
    if tid == 0 :
        print aggr
    else:
        print aggr[tid]
    print '\n'

    opt = raw_input("Write aggregated counters to csv format(Y/N) ?  ")
    if opt == "Y" or opt == "y":
        print ""
    else:
        return()

    name = raw_input("Please Enter a file name to print flows to:\t")
    filename = '%s.csv' % name

    with open(filename, 'w') as csvfile:
        fieldnames = ['dpid', 'hash', 'in_port', 'dl_src', 'dl_dst', 'dl_type', 'dl_vlan', 'nw_proto', 'nw_src',
                      'nw_dst', 'nw_tos', 'tp_src', 'tp_dst', 'Packet_Counter', 'Packet_In','tenant', 'physicalDPID']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for ten_id, fr in aggr.iteritems():
            if tid == 0 or ten_id == tid:
                for kk, vv in fr.iteritems():
                    for l, w in vv.iteritems():
                        b = w['match']
                        b['dpid'] = kk
                        b['hash'] = l
                        b['Packet_Counter'] = w['counters']['counterX']
                        b['Packet_In'] = w['counters']['Packet_In']
                        b['tenant'] = w['tenant']
                        b['physicalDPID'] = w['physicalDPID']
                        writer.writerow(b)
    print "\n\n Aggregate Successfull!\n\n"

@timeout(1)
def get_samplewithnoinforate():
    try:
        activate_server()
        #time.sleep(0.5)
        print server.get_samplewithnoinforate()
        return
    except TimeoutError:
        print "Timeout Error from client's get_samplewithnointrorate."
        get_samplewithnoinforate()

if __name__ == "__main__":
    global producer
    register_queue()
    print "Client is ready."
    update_data()
    while True:
        print 'Enter:'
        print '1:\t for active counters'
        print '2:\t for expired counters'
        print '3:\t to update counters'
        print '4:\t to get sample with no info rate'
        print '5:\t to aggregate counters'
        print '6:\t to exit\n\n'

        choice = raw_input("\nPlease Enter a valid option:\t")
        print "\n\n"
        choices = ['1', '2', '3', '4', '5', '6']
        option = {'1': ret_active,
                  '2': ret_expired,
                  '3': update_data,
                  '4': get_samplewithnoinforate,
                  '5': aggregate,
                  '6': sys.exit}

        while choice not in choices:
            choice = raw_input("Please Enter a valid option:\t")
            print "\n\n"
        option[choice]()
        choice = None




