#!/usr/bin/python

"""
Create SCENARIO 03
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/24')

    info(
"""
Creating the folow topology:

               +------------+
+----+         | controller |                      +----+
| h1 |         +-----:------+                  /---| h3 |
+----+           +---:---+     +----+    +----+    +----+
      \----------| swof1 |-----| r2 |----| s1 |
                 +-------+     +----+    +----+    +----+
+----+              |                       |------| h4 |
| h2 |--------------|                              +----+
+----+
------------------------------------------------------------------------
DEVICE          NAME            IP:PORT         	DESCRIPTION
------------------------------------------------------------------------
switch_OpenFlow swof1           10.0.0.250/24      
controller      controller      127.0.0.1:6633
r2          	r2            	10.0.0.254/24
            	            	192.168.111.254/24
h1          	h1          	10.0.0.1/24
h2          	h2          	10.0.0.2/24
h3          	h3          	192.168.111.1/24
h4          	h4          	192.168.111.2/24
------------------------------------------------------------------------
""")

    info('*** Adding controller\n' )
    controller=RemoteController('controller', ip='127.0.0.1', protocol='tcp', port=6633)
    net.addController(controller)


    info('*** Add switches\n')
    swof1 = net.addSwitch('swof1', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')

    info('*** Add router\n')
    r2 = net.addHost('r2', cls=Node, ip='10.0.0.254/24')
    
    info('*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1/24', defaultRoute='via 10.0.0.254')
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2/24', defaultRoute='via 10.0.0.254')
    h3 = net.addHost('h3', cls=Host, ip='192.168.111.1/24', defaultRoute='via 192.168.111.254')
    h4 = net.addHost('h4', cls=Host, ip='192.168.111.2/24', defaultRoute='via 192.168.111.254')

    info('*** Add links\n')
    net.addLink(swof1, r2)
    net.addLink(s1, r2)

    net.addLink(swof1, h1)
    net.addLink(swof1, h2)
    
    net.addLink(s1, h3)
    net.addLink(s1, h4)

    info('*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')

    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('swof1').start([controller])
    net.get('s1').start([])

    info('*** Post configure switches and hosts\n')
    swof1.cmd('ifconfig swof1 10.0.0.250/24 up')

    info('*** Config router\n')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    r2.cmd('ifconfig r2-eth0 down && ifconfig r2-eth0 10.0.0.254/24 up')
    r2.cmd('ifconfig r2-eth1 down && ifconfig r2-eth1 192.168.111.254/24 up')

    CLI(net)
    
    info('########## Stopping CLI ##########\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

