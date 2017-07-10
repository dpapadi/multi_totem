#!/usr/bin/python

#testing topology created through Mininet

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import lg, setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

CORES = {
  'S12' : {'dpid': '0000000000000012', 'id': '12' },
  'S123': {'dpid': '0000000000000123', 'id': '123'},
  'S13' : {'dpid': '0000000000000013', 'id': '13' },
  'S23' : {'dpid': '0000000000000023', 'id': '23' },
  'S34' : {'dpid': '0000000000000034', 'id': '34' }
  }

hosts = {
    'H11' : {'mac': '000000001211', 'ip': '10.0.1.1', 'switch': 'S12'},
    'H12' : {'mac': '000000001312', 'ip': '10.0.1.2', 'switch': 'S13'},
    'H21' : {'mac': '000000001221', 'ip': '10.0.2.1', 'switch': 'S12'},
    'H22' : {'mac': '000000002322', 'ip': '10.0.2.2', 'switch': 'S23'},
    'H31' : {'mac': '000000001331', 'ip': '10.0.3.1', 'switch': 'S13'},
    'H32' : {'mac': '000000003432', 'ip': '10.0.3.2', 'switch': 'S34'},
    'H41' : {'mac': '000000003441', 'ip': '10.0.4.1', 'switch': 'S34'},
    'H42' : {'mac': '000000003442', 'ip': '10.0.4.2', 'switch': 'S34'}
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
            self.cores[switch] = self.addSwitch(switch, dpid=(CORES[switch]['dpid']))


        # Add hosts and connect them to their core switch
        #for switch in CORES:
         #   for count in xrange(1, FANOUT + 1):
                # Add hosts
          #      host = '%s_%s' % (switch, count)
           #     ip = '10.0.%s.%s' % (count, CORES[switch]['id'])
            #    mac = CORES[switch]['dpid'][4:] % count
             #   h = self.addHost(host, ip=ip, mac=mac)
                # Connect hosts to core switches
              #  self.addLink(h, self.cores[switch])

    print "\n\n"
    print hosts
    print "\n\n"

        #add hosts
        for host in hosts:
            h = self.addHost(host, ip=hosts[host]['ip'], mac=hosts[host]['mac'])
            self.addLink(h, self.cores[hosts[host]['switch']])

             # Connect core switches
        self.addLink(self.cores['S12'], self.cores['S123'])
        self.addLink(self.cores['S13'], self.cores['S123'])
        self.addLink(self.cores['S23'], self.cores['S123'])
        self.addLink(self.cores['S23'], self.cores['S34'])

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