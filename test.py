#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf

import time

def myNetwork():

    net = Mininet(topo=None, build=False, ipBase='10.0.0.0/8')

    info( '*** Add controller\n' )
    c0 = net.addController(name='c0', controller=RemoteController, ip='192.168.56.1', port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, mac='00:00:00:00:00:01', ip='10.0.1.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, mac='00:00:00:00:00:02', ip='10.0.2.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, mac='00:00:00:00:00:03', ip='10.0.3.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, mac='00:00:00:00:00:04', ip='10.0.4.4', defaultRoute=None)
	
	
    info( '*** Add links\n')
    bw8 = {'bw':8}
    bw6 = {'bw':6}
    bw4 = {'bw':4}
    bw2 = {'bw':2}
    net.addLink(h1, s1, cls=TCLink, **bw8)
    net.addLink(h2, s2, cls=TCLink, **bw8)
    net.addLink(h3, s3, cls=TCLink, **bw8)
    net.addLink(h4, s4, cls=TCLink, **bw8)
    net.addLink(s1, s2, cls=TCLink, **bw8)
    net.addLink(s2, s3, cls=TCLink, **bw6)
    net.addLink(s2, s4, cls=TCLink, **bw4)
    net.addLink(s3, s4, cls=TCLink, **bw2)

    info( '*** Start network\n')
    net.build()
	
    info( '*** Start controller\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Start switches\n')

    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])


    time.sleep(2);


    info( '*** Configuring switches\n')

    hostsAll = net.hosts
    outfiles, errfiles = {}, {}
	
    net.iperf((h1, h2))
    net.iperf((h1, h3))
    net.iperf((h1, h4))
	
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
