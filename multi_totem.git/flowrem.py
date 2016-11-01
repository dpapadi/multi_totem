from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
from pox.openflow import *
from pox.forwarding import l2_learning
from kafka.client import SimpleClient
from kafka.producer import SimpleProducer
import os
import pickle
import jsonrpclib
import time


# Create Loggers
log = core.getLogger()
log1 = core.getLogger("Flow Installed")
log2 = core.getLogger("Flow Removed")

# Create a new jsonrpclib.Server object, bound to an IP
# server = jsonrpclib.Server('http://localhost:8085')

#for OpenVirteX confirmation, tid-->tenant id, passwd--> password
OVX_par = {'tid' : 0, 'pass' : ""}


class CustomEvent(Event):
    """
    Our own custom event
    """

    def __init__(self, connection, ofp):
        Event.__init__(self)
        self.connection = connection
        self.ofp = ofp
        self.dpid = connection.dpid


class EventSourcer (EventMixin):
    """
    Our event raise class. Can only raise CustomEvent
    """
    _eventMixin_events = set([
    CustomEvent,
    ])

# Create a new object of type EventSourcer
handler = EventSourcer()


class FlowRemovalHandler (EventMixin):
    """
    The core functionality of our module.
    Key methods are the handlers for Custom Events and Flow Removed Events
    Each one serializes the ofp.match and performs an RPC to Flow Cache
    """
    def __init__(self):
        self.listenTo(core.openflow)
        self.listenTo(handler)
        log.debug("...Enabling Flow Removal Module...")

    def _handle_CustomEvent(self, event):
        # log1.debug('Flow Installed on switch: %s', event.connection)
        # log1.debug(event.ofp.match)

        args = ()
        connction = event.connection
        args = ("construct_new_entry", event.ofp.match, str(connction.dpid), str(time.time()), OVX_par['tid'], OVX_par['pass']) #send tid and passwd for pratical and security issues
        b = pickle.dumps(args)
        #server.construct_new_entry(b)
        producer.send_messages("test1", b)
        # a = server.construct_new_entry(b)
        # c = pickle.loads(a)

    def _handle_FlowRemoved(self, event):

        args = ()
        connection = event.connection
        args = ("move_to_expired", event.ofp.match, str(connection.dpid), str(time.time()),OVX_par['tid'], OVX_par['pass']) #send tid and passwd for pratical and security issues
        b = pickle.dumps(args)
        producer.send_messages("test1", b)
        #a = server.move_to_expired(b)
        #c = pickle.loads(a)
        log2.debug('Flow Removed from switch: %s', event.connection)
        # log2.debug(c)


def launch(tid=0, passwd="", queue="localhost:9092"):
    """
    Starting the module
    """
    tryagain = True
    OVX_par['tid'] = tid
    OVX_par['pass'] = passwd
    while tryagain:
        try:
            kafka = SimpleClient(queue)
            global producer
            producer = SimpleProducer(kafka)
            tryagain = False
        except Exception:
            print "Kafka is unavailable at the moment."
            time.sleep(2)
    #producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092')
    core.registerNew(FlowRemovalHandler)


def invoker(con, msg):
    """
    When called raises CustomEvent
    """
    handler.raiseEvent(CustomEvent(con, msg))
