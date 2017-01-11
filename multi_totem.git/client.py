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

# Active Flows
active = {}

# Expired Flows
expired = {}

def register_queue():
    tryagain = True
    while tryagain:
        try:
            #kafka = KafkaClient(bootstrap_servers="localhost:9092")
            global producer
            producer = KafkaProducer(bootstrap_servers="localhost:9092")
            tryagain = False
        except Exception:
            print "Kafka is unavailable at the moment."
            time.sleep(5)
    return

@timeout()
def update_data():
    try:
        activate_server()
        time.sleep(0.5)
        a = server.checkout()
        args = pickle.loads(a)
        global active
        active = args[0]
        global expired
        expired = args[1]
        print "Data updated"
        print "\n\n"
        return (active, expired)
    except TimeoutError:
        print "Timeout Error from client's update data."
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
    try:
        tid = raw_input("Enter Tenant ID (0 for all tenant counters) or r to return: ")
        if tid == "r":
            return
        elif int(tid) == 0:
            print "\nactive: "
            print active
        else:
            print "\nactive: "
            print active[int(tid)]
        print "\n\n"
    except Exception:
        print "\n\nSomething went wrong. Please enter a valid option.\n\n"
        ret_active()
    return

def ret_expired():
    try:
        tid = raw_input("Enter Tenant ID (0 for all tenant counters) or r to return: ")
        if tid == "r":
            return
        elif int(tid) == 0:
            print "\nexpired: "
            print expired
        else:
            print "\nexpired: "
            print expired[int(tid)]
        print "\n\n"
    except Exception:
        print "\n\nSomething went wrong. Please enter a valid option.\n\n"
        ret_expired()
    return

@timeout(1)
def get_samplewithnoinforate():
    try:
        activate_server()
        time.sleep(0.5)
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
        print '5:\t to exit\n\n'

        choice = raw_input("Please Enter a valid option:\t")
        print "\n\n"
        choices = ['1', '2', '3', '4', '5']
        option = {'1': ret_active,
                  '2': ret_expired,
                  '3': update_data,
                  '4': get_samplewithnoinforate,
                  '5': sys.exit}

        while choice not in choices:
            choice = raw_input("Please Enter a valid option:\t")
            print "\n\n"
        option[choice]()
        choice = None




