from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.addresses import EthAddr

log = core.getLogger() 

#MAC 01 = server
#MAC 02 = client
#MAC 03 = guest
rules =	[ ['00:00:00:00:00:01','00:00:00:00:00:03'],
	  ['00:00:00:00:00:03','00:00:00:00:00:01'] ]

class Firewall_L2 (EventMixin):
    
  def __init__ (self):
    self.listenTo(core.openflow)

  def _handle_ConnectionUp (self, event):
    for rule in rules:
      block = of.ofp_match()
      block.dl_src = EthAddr(rule[0])
      block.dl_dst = EthAddr(rule[1])
      flow_mod = of.ofp_flow_mod()
      flow_mod.match = block
      event.connection.send(flow_mod)

def launch ():
  core.registerNew(Firewall_L2)

