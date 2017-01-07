#!/usr/bin/python

import sys
import pickle
import csv
import time
import jsonrpclib

server = jsonrpclib.Server('http://localhost:8085')

def register_queue():
    try:
        kafka = SimpleClient(sys.argv[2])
        global producer
        producer = SimpleProducer(kafka)
        global tryagain
        tryagain = False
        return
    except Exception:
        print "Kafka is unavailable at the moment."
        return


if __name__ == "__main__":
    done = True
    a = len(sys.argv)
    global trygain
    tryagain = True
    global producer
    while tryagain:
        register_queue()
    print "Client is ready."
    try:
        producer.send_messages("client", True)
    except:
        print "Error in queue!"
        tryagain = True
    while done:
        (msg, done) = server.checkout()
    print msg

