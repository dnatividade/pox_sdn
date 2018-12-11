#!/usr/bin/python

"""
Create SCENARIO 02
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
                         
                +----+   
                | c1 |   
                +--:-+                      +----+
                   :     /------------------| h3 |
+----+         +---:---+/                   +----+      
| h1 |---------| swof1 |---
+----+         +-------+   \      
                |   | |     \              +----+
                |   | |      \-------------| h4 |
+----+          |   | |                    +----+
| h2 |-----------   | |     +----+    
+----+              | |-----| h5 |
                    |       +----+
            +----+  |        
            | h6 |--|
            +----+
------------------------------------------------------------------------
DEVICE          NAME            IP:PORT         	DESCRIPTION
------------------------------------------------------------------------
switch_OpenFlow swof1           10.10.0.254/24
                                10.20.0.254/24
                                10.30.0.254/24
controller      c1              127.0.0.1:6633
h1          	h1          	10.10.0.1/24
h2          	h2          	10.10.0.2/24
h3          	h3          	10.20.0.3/24
h4          	h4          	10.20.0.4/24
h5          	h5          	10.30.0.5/24
h6          	h6          	10.30.0.6/24
------------------------------------------------------------------------
""")

    info('*** Adding controller\n' )
    controller=RemoteController('controller', ip='127.0.0.1', protocol='tcp', port=6633)
    net.addController(controller)
    
    info('*** Add switches\n')
    swof1 = net.addSwitch('swof1', cls=OVSKernelSwitch)

    info('*** Add hosts\n')
    h1  = net.addHost('h1', cls=Host, ip='10.10.0.1/24', mac='00:00:00:00:00:01')
    h2  = net.addHost('h2', cls=Host, ip='10.10.0.2/24', mac='00:00:00:00:00:02')
    h3  = net.addHost('h3', cls=Host, ip='10.20.0.3/24', mac='00:00:00:00:00:03')
    h4  = net.addHost('h4', cls=Host, ip='10.20.0.4/24', mac='00:00:00:00:00:04')
    h5  = net.addHost('h5', cls=Host, ip='10.30.0.5/24', mac='00:00:00:00:00:05')
    h6  = net.addHost('h6', cls=Host, ip='10.30.0.6/24', mac='00:00:00:00:00:06')

    info('*** Add links\n')
    net.addLink(swof1, h1)
    net.addLink(swof1, h2)
    net.addLink(swof1, h3)
    net.addLink(swof1, h4)
    net.addLink(swof1, h5)
    net.addLink(swof1, h6)

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('swof1').start([controller])

    info('*** Post configure hosts\n')
    h1.cmd('route add default gw 10.10.0.254')
    h2.cmd('route add default gw 10.10.0.254')
    h3.cmd('route add default gw 10.20.0.254')
    h4.cmd('route add default gw 10.20.0.254')
    h5.cmd('route add default gw 10.30.0.254')
    h6.cmd('route add default gw 10.30.0.254')

    CLI(net)
    
    info('########## Stopping CLI ##########\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

