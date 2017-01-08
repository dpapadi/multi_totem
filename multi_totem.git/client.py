#!/usr/bin/python

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
        while tryagain:
            kafka = KafkaClient(bootstrap_servers="localhost:9092")
            global producer
            producer = KafkaProducer(bootstrap_servers="localhost:9092")
            tryagain = False
        #except Exception:
         #   print "Kafka is unavailable at the moment."
          #  time.sleep(5)
    return

def update_data():
    a = server.checkout()
    args = pickle.loads(a)
    global active
    active = args[0]
    global expired
    expired = args[1]
    print "Data updated"
    print "\n\n"
    return (active, expired)

def activate_server():
    #try:
    producer.send_messages("client", "hi")
    #except:
       # print "Error in queue!"
     #   register_queue()
      #  return
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

if __name__ == "__main__":
    global producer
    register_queue()
    print "Client is ready."
    activate_server()
    update_data()
    while True:
        print 'Enter:'
        print '1:\t for active counters'
        print '2:\t for expired counters'
        print '3:\t to update counters'
        print '4:\t to exit\n\n'

        choice = raw_input("Please Enter a valid option:\t")
        print "\n\n"
        choices = ['1', '2', '3', '4']
        option = {'1': ret_active,
                  '2': ret_expired,
                  '3': update_data,
                  '4': sys.exit}

        while choice not in choices:
            choice = raw_input("Please Enter a valid option:\t")
            print "\n\n"
        activate_server()
        option[choice]()
        choice = None




