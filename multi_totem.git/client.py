#!/usr/bin/python

import sys
import pickle
import csv
import time
import jsonrpclib
from kafka.client import SimpleClient
from kafka.producer import SimpleProducer

server = jsonrpclib.Server('http://localhost:8085')

def register_queue():
    try:
        kafka = SimpleClient("localhost:9092")
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
    global trygain
    tryagain = True
    loop = True
    global producer
    while tryagain:
        register_queue()
    print "Client is ready."
    while loop:
        try:
            producer.send_messages("client", True)
            loop = False
        except:
            print "Error in queue!"
            loop = True
    while done:
        a = server.checkout()
        (msg, done) = pickle.loads(a)
    print msg

