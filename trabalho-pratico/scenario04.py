#!/usr/bin/python

"""
Create SCENARIO 04
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
                   ipBase='10.0.0.0/8')

    info(
"""
Creating the folow topology:
                                    +----+
                +----+           /--| h3 |         
                | c1 |       +--+   +----+  +----+
                +--:-+    /--|s2|-----------| h4 |      
                   :     /   +--+           +----+
+----+         +---:---+/        +-------+                      +----+
| h1 |----|    | swof1 |---------| swof2 |......................| c2 |
+----+  +--+   +-------+         +-------+\     +--+            +----+
        |s1|-----|  |                  |   \----|s4|   +----+
        +--+        | +--+    +----+   |        +--+---| h7 |      
+----+    |         |-|s3|----| h6 |   |          |    +----+
| h2 |----|           +--+    +----+   |          |   +----+
+----+                  |              |          |---| h8 |
                        |              |              +----+
                     +----+            |
                     | h5 |        +-------+    +--+  +----+       
                     +----+     |--| swop3 |----|s6|--| h11|
  +----+                +--+    |  +-------+    +--+  +----+ 
  | h9 |----------------|s5|----|       :         |     +----+
  +----+                +--+            :         |-----| h12|
           +----+         |             :               +----+   +----+
           | h10|---------|             :........................| c3 |
           +----+                                                +----+
------------------------------------------------------------------------
DEVICE          NAME            IP:PORT         	DESCRIPTION
------------------------------------------------------------------------
switch_OpenFlow swof1           10.255.255.1/8
switch_OpenFlow swof2           10.255.255.2/8
switch_OpenFlow swof3           10.255.255.3/8      
controller      c1              127.0.0.1:6631
controller      c2              127.0.0.2:6632
controller      c3              127.0.0.2:6633
switch legacy  	s1          	---
switch legacy  	s2          	---
switch legacy  	s3         	---
switch legacy  	h4          	---
switch legacy  	S5          	---
switch legacy  	s6          	---
h1          	h1          	10.0.0.1/8
h2          	h2          	10.0.0.2/8
h3          	h3          	10.0.0.3/8
h4          	h4          	10.0.0.4/8
h5          	h5          	10.0.0.5/8
h6          	h6          	10.0.0.6/8
h7          	h7          	10.0.0.7/8
h8          	h8          	10.0.0.8/8
h9          	h9          	10.0.0.9/8
h10         	h10         	10.0.0.10/8
h11         	h11         	10.0.0.11/8
h12         	h12         	10.0.0.12/8

------------------------------------------------------------------------
""")

    info('*** Adding controller\n' )
    c1=RemoteController('c1', ip='127.0.0.1', protocol='tcp', port=6631)
    net.addController(c1)
    
    c2=RemoteController('c2', ip='127.0.0.2', protocol='tcp', port=6632)
    net.addController(c2)

    c3=RemoteController('c3', ip='127.0.0.3', protocol='tcp', port=6633)
    net.addController(c3)


    info('*** Add switches\n')
    swof1 = net.addSwitch('swof1', cls=OVSKernelSwitch)
    s1    = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2    = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
    s3    = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')

    swof2 = net.addSwitch('swof2', cls=OVSKernelSwitch)
    s4    = net.addSwitch('s4', cls=OVSKernelSwitch, failMode='standalone')

    swof3 = net.addSwitch('swof3', cls=OVSKernelSwitch)
    s5    = net.addSwitch('s5', cls=OVSKernelSwitch, failMode='standalone')
    s6    = net.addSwitch('s6', cls=OVSKernelSwitch, failMode='standalone')

    info('*** Add hosts\n')
    h1  = net.addHost('h1', cls=Host, ip='10.0.0.1/8', mac='00:00:00:00:00:01')
    h2  = net.addHost('h2', cls=Host, ip='10.0.0.2/8', mac='00:00:00:00:00:02')
    h3  = net.addHost('h3', cls=Host, ip='10.0.0.3/8', mac='00:00:00:00:00:03')
    h4  = net.addHost('h4', cls=Host, ip='10.0.0.4/8', mac='00:00:00:00:00:04')
    h5  = net.addHost('h5', cls=Host, ip='10.0.0.5/8', mac='00:00:00:00:00:05')
    h6  = net.addHost('h6', cls=Host, ip='10.0.0.6/8', mac='00:00:00:00:00:06')

    h7  = net.addHost('h7', cls=Host, ip='10.0.0.7/8', mac='00:00:00:00:00:07')
    h8  = net.addHost('h8', cls=Host, ip='10.0.0.8/8', mac='00:00:00:00:00:08')

    h9  = net.addHost('h9',  cls=Host, ip='10.0.0.9/8',  mac='00:00:00:00:00:09')
    h10 = net.addHost('h10', cls=Host, ip='10.0.0.10/8', mac='00:00:00:00:00:10')
    h11 = net.addHost('h11', cls=Host, ip='10.0.0.11/8', mac='00:00:00:00:00:11')
    h12 = net.addHost('h12', cls=Host, ip='10.0.0.12/8', mac='00:00:00:00:00:12')

    info('*** Add links\n')
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s2, h3)
    net.addLink(s2, h4)
    net.addLink(s3, h5)
    net.addLink(s3, h6)

    net.addLink(s4, h7)
    net.addLink(s4, h8)

    net.addLink(s5, h9)
    net.addLink(s5, h10)
    net.addLink(s6, h11)
    net.addLink(s6, h12)

    net.addLink(swof1, s1)
    net.addLink(swof1, s2)
    net.addLink(swof1, s3)
    
    net.addLink(swof2, s4)

    net.addLink(swof3, s5)
    net.addLink(swof3, s6)


    net.addLink(swof2, swof1) #2 #4
    net.addLink(swof2, swof3) #3 #3

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('swof1').start([c1])
    net.get('s1').start([])
    net.get('s2').start([])
    net.get('s3').start([])

    net.get('swof2').start([c2])
    net.get('s4').start([])

    net.get('swof3').start([c3])
    net.get('s5').start([])
    net.get('s6').start([])

    info('*** Post configure switches\n')
    #swof1.cmd('ifconfig swof1 10.255.255.1/8')
    #swof2.cmd('ifconfig swof2 10.255.255.2/8')
    #swof3.cmd('ifconfig swof2 10.255.255.3/8')

    CLI(net)
    
    info('########## Stopping CLI ##########\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

