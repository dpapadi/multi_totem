#!/usr/bin/python

import sys
import pickle
import csv
import time
import jsonrpclib
from kafka.client import SimpleClient
from kafka.producer import SimpleProducer

server = jsonrpclib.Server('http://localhost:8085')

# Active Flows
active = {}

# Expired Flows
expired = {}

def register_queue():
    tryagain = True
    while tryagain:
        try:
            kafka = SimpleClient("localhost:9092")
            global producer
            producer = SimpleProducer(kafka)
            tryagain = False
        except Exception:
            print "Kafka is unavailable at the moment."
            time.sleep(5)
    return

def update_data():
    done = True
    while done:
        a = server.checkout()
        args = pickle.loads(a)
        global active
        active = args[0]
        global expired
        expired = args[1]
        done = args[2]
    print "Data updated"
    print "\n\n"
    return (active, expired)

def activate_server():
    try:
        producer.send_messages("client", "hi")
    except:
        print "Error in queue!"
        register_queue()

def ret_active():
    print "active: " + str(active)
    print "\n\n"
    return

def ret_expired():
    print "expired: " + str(expired)
    print "\n\n"
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




