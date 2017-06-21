#!/usr/bin/python

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import lg, setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

CORES = {
  'S1': {'dpid': '000000000000010%s'},
  'S2': {'dpid': '000000000000020%s'},
  'S3': {'dpid': '000000000000030%s'},
  'S4': {'dpid': '000000000000040%s'},
  'S5': {'dpid': '000000000000050%s'}
  }

FANOUT = 5

class TestingTopo(Topo):

    def __init__(self, enable_all = True):
        "Create my testing topology."

        # Add default members to class.
         super(TestingTopo, self).__init__()

         # Add core switches
         self.cores = {}
         for switch in CORES:
            self.cores[switch] = self.addSwitch(switch, dpid=(CORES[switch]['dpid'] % '0'))

         #used to customize host ips
         mycount = 1

         # Add hosts and connect them to their core switch
         for switch in CORES:
             for count in xrange(1, FANOUT + 1):
                 # Add hosts
                 host = '%s_%s' % (switch, count)
                 ip = '%s.0.0.%s' % (count, mycount)
                 mac = CORES[switch]['dpid'][4:] % mycount
                 h = self.addHost(host, ip=ip, mac=mac)
                 # Connect hosts to core switches
                 self.addLink(h, self.cores[switch])
             mycount+=1

             # Connect core switches
         self.addLink(self.cores['S1'], self.cores['S2'])
         self.addLink(self.cores['S1'], self.cores['S3'])
         self.addLink(self.cores['S2'], self.cores['S3'])
         self.addLink(self.cores['S2'], self.cores['S4'])
         self.addLink(self.cores['S3'], self.cores['S4'])
         self.addLink(self.cores['S4'], self.cores['S5'])

if __name__ == '__main__':
    topo = TestingTopo()
    ip = '127.0.0.1'
    port = 6633
    c = RemoteController('c', ip=ip, port=port)
    net = Mininet(topo=topo, autoSetMacs=True, xterms=False, controller=None)
    net.addController(c)
    net.start()
    print "Hosts configured with IPs, switches pointing to OpenVirteX at %s:%s" % (ip, port)
    CLI(net)
    net.stop()