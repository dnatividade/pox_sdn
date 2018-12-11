#!/usr/bin/python

"""
Create SCENARIO 01
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

                   +------------+
                   | controller |            +--------+
                   +-----:------+   /--------| client |
+-------+            +---:---+-----/         +--------+
| server |-----------| swof1 |
+--------+           +-------+----\          +---------+
                                   \---------|  guest  |
                                             +---------+

------------------------------------------------------------------------
DEVICE          NAME            IP:PORT         	DESCRIPTION
------------------------------------------------------------------------
switch_OpenFlow swof1           10.0.0.254/8      
controller      controller      127.0.0.1:6633

server          server          10.0.0.1/8
client          client          10.0.0.2/8
guest           guest           10.0.0.3/8
------------------------------------------------------------------------
""")

    info( '*** Adding controller\n' )
    controller=RemoteController('controller', ip='127.0.0.1', protocol='tcp', port=6633)
    net.addController(controller)

    info( '*** Add switches\n')
    swof1 = net.addSwitch('swof1', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    server = net.addHost('server', cls=Host, ip='10.0.0.1', defaultRoute=None, mac='00:00:00:00:00:01')
    client = net.addHost('client', cls=Host, ip='10.0.0.2', defaultRoute=None, mac='00:00:00:00:00:02')
    guest  = net.addHost('guest',  cls=Host, ip='10.0.0.3', defaultRoute=None, mac='00:00:00:00:00:03')

    info( '*** Add links\n')
    net.addLink(swof1, server)
    net.addLink(swof1, client)
    net.addLink(swof1, guest)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('swof1').start([controller])

    info( '*** Post configure switches and hosts\n')
    swof1.cmd('ifconfig swof1 10.0.0.254')

    CLI(net)
    
    info('########## Stopping CLI ##########\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

