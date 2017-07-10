#!/usr/bin/python

#testing topology created through Mininet

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import lg, setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

CORES = {
  's1'   : {'dpid': '0000000000000001'}, #nh --> number of hosts
  's2'   : {'dpid': '0000000000000002'},
  's3'   : {'dpid': '0000000000000003'},
  's4'   : {'dpid': '0000000000000004'},
  'int1' : {'dpid': '0000000000000005'},
  'int2' : {'dpid': '0000000000000006'},
  'int3' : {'dpid': '0000000000000007'},
  'gtw'  : {'dpid': '0000000000000008'}
  }

hosts = {
    'h1'     : {'mac': '00000000001%s', 'ip': '10.0.1.%s', 'switch': 's1'  , 'nh': 4},
    'h2'     : {'mac': '00000000002%s', 'ip': '10.0.2.%s', 'switch': 's2'  , 'nh': 4},
    'h3'     : {'mac': '00000000003%s', 'ip': '10.0.3.%s', 'switch': 's3'  , 'nh': 4},
    'h4'     : {'mac': '00000000004%s', 'ip': '10.0.4.%s', 'switch': 's4'  , 'nh': 4},
    'int1'   : {'mac': '00000000005%s', 'ip': '10.0.5.1' , 'switch': 'int1', 'nh': 1},
    'int2'   : {'mac': '00000000006%s', 'ip': '10.0.6.1' , 'switch': 'int2', 'nh': 1},
    'int3'   : {'mac': '00000000007%s', 'ip': '10.0.7.1' , 'switch': 'int3', 'nh': 1},
    'hgtw'   : {'mac': '00000000008%s', 'ip': '10.0.8.%s', 'switch': 'gtw' , 'nh': 4 }
}



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

        #add hosts
        for host in hosts:
            for x in range(1, hosts[host]['nh']+1):
                hst = '%s%s' % (host, str(x))
                ip = hosts[host]['ip'] % str(x)
                mac = hosts[host]['mac'] % str(x)
                h = self.addHost(hst, ip=ip, mac=mac)
                self.addLink(h, self.cores[hosts[host]['switch']])

             # Connect core switches
        self.addLink(self.cores['int1'], self.cores['s1'])
        self.addLink(self.cores['int1'], self.cores['int2'])
        self.addLink(self.cores['int1'], self.cores['int3'])
        self.addLink(self.cores['int1'], self.cores['s3'])
        self.addLink(self.cores['int2'], self.cores['s2'])
        self.addLink(self.cores['int2'], self.cores['int3'])
        self.addLink(self.cores['int2'], self.cores['gtw'])
        self.addLink(self.cores['int3'], self.cores['s4'])
        self.addLink(self.cores['int3'], self.cores['gtw'])


if __name__ == '__main__':
    topo = TestingTopo()
    ip = '127.0.0.1'
    port = 6633
    c = RemoteController('c', ip=ip, port=port)
    net = Mininet(topo=topo, autoSetMacs=True, xterms=False, controller=None)
    net.addController(c)
    net.start()
    print "Hosts configured with IPs, switches pointing to remote controller at %s:%s" % (ip, port)
    CLI(net)
    net.stop()