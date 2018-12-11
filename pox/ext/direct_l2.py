from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.addresses import EthAddr, IPAddr

log = core.getLogger() 

#     0        1       2         3        4         5      6       7        8        9          10       11
# priority, sw_port, mac_src, mac_dst, eth_type, vlanID, ip_src, ip_dst, ip_prot, tcp_sport, TCP_dport, action
rules = [ ['*','1','*','*','*','*','*','*','*','*','*','2'],
          ['*','2','*','*','*','*','*','*','*','*','*','1'] ]

class FlowTable (EventMixin):
    
  def __init__ (self):
    self.listenTo(core.openflow)

  def _handle_ConnectionUp (self, event):
    for r in rules:
      msg = of.ofp_flow_mod()
      
      if r[0]  != '*':  msg.priority = int(r[0])
      if r[1]  != '*':  msg.in_port  = int(r[1])
      if r[2]  != '*':  msg.dl_src   = EthAddr(r[2])
      if r[3]  != '*':  msg.dl_dst   = EthAddr(r[3])
      if r[4]  != '*':  msg.match.dl_type  = int(r[4], 16)
      if r[5]  != '*':  msg.dl_vlan        = int(r[5])
      if r[6]  != '*':  msg.match.nw_src   = IPAddr(r[6])
      if r[7]  != '*':  msg.match.nw_dst   = IPAddr(r[7])
      if r[8]  != '*':  msg.match.nw_proto = int(r[8])
      if r[9]  != '*':  msg.match.tp_src   = int(r[9])
      if r[10] != '*':  msg.match.tp_dst   = int(r[10])
      if r[11] != '*':  msg.actions.append(of.ofp_action_output(port = int(r[11])))
#      if r[11] != '*':  msg.actions.append(of.ofp_action_output('drop'))

      event.connection.send(msg)


def launch ():
  core.registerNew(FlowTable)

