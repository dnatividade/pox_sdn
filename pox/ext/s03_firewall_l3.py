"""
Block TCP/UDP ports
version: 2018.11.24
"""
 
from pox.core import core
 
# Set of ports to block
block_ports = set()
 
def block_handler (event):

  ipp  = event.parsed.find('ipv4')
  tcpp = event.parsed.find('tcp')
  udpp = event.parsed.find('udp')
  
  # Put here your TCP rules ########################################
  if not ipp:
    return

  if tcpp: 
    if ipp.dstip == "10.0.0.1" and tcpp.dstport == 8817 and (ipp.srcip == "192.168.111.1" or ipp.srcip == "192.168.111.2"):
      core.getLogger("firewall_l3").error("Traffic TCP blocked: %s:%s -> %s:%s", ipp.srcip, tcpp.srcport, ipp.dstip, tcpp.dstport)
      event.halt = True
  
#    if ipp.dstip == "10.0.0.1" and tcpp.dstport == 88 and (ipp.srcip == "192.168.111.1" or ipp.srcip == "192.168.111.2"):
#      core.getLogger("firewall_l3").error("Traffic TCP blocked: %s:%s -> %s:%s", ipp.srcip, tcpp.srcport, ipp.dstip, tcpp.dstport)
#      event.halt = True
  ########################################################################
  
  # Put here your UDP rules ###############################################
  if udpp:
    if ipp.dstip == "10.0.0.1" and udpp.dstport == 53 and (ipp.srcip == "192.168.111.1" or ipp.srcip == "192.168.111.2"):
      core.getLogger("firewall_l3").error("Traffic UDP blocked: %s:%s -> %s:%s", ipp.srcip, udpp.srcport, ipp.dstip, udpp.dstport)
      event.halt = True
  
#    if ipp.dstip == "10.0.0.1" and udpp.dstport == 5001 and (ipp.srcip == "192.168.111.1" or ipp.srcip == "192.168.111.2"):
#      core.getLogger("firewall_l3").error("Traffic UDP blocked: %s:%s -> %s:%s", ipp.srcip, udpp.srcport, ipp.dstip, udpp.dstport)
#      event.halt = True
  ########################################################################

 
#  if tcpp.srcport in block_ports or tcpp.dstport in block_ports:
def unblock (*ports):
  block_ports.difference_update(ports)
 
def block (*ports):
  block_ports.update(ports)
 
def launch (ports = ''):
 
  # Add ports from commandline to list of ports to block
  block_ports.update(int(x) for x in ports.replace(",", " ").split())
 
  # Add functions to Interactive so when you run POX with py, you
  # can easily add/remove ports to block.
  core.Interactive.variables['block'] = block
  core.Interactive.variables['unblock'] = unblock
 
  # Listen to packet events
  core.openflow.addListenerByName("PacketIn", block_handler)



