"""
RULES FOR C1
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.addresses import EthAddr, IPAddr

log = core.getLogger() 

#     0        1       2         3        4         5      6       7        8        9          10       11
# priority, sw_port, mac_src, mac_dst, eth_type, vlanID, ip_src, ip_dst, ip_prot, tcp_sport, TCP_dport, action
rules = [ ['100','*','*','00:00:00:00:00:01','*','*','*','*','*','*','*','1'],
          ['100','*','*','00:00:00:00:00:02','*','*','*','*','*','*','*','1'],

          ['100','*','*','00:00:00:00:00:03','*','*','*','*','*','*','*','2'],
          ['100','*','*','00:00:00:00:00:04','*','*','*','*','*','*','*','2'],

          ['100','*','*','00:00:00:00:00:05','*','*','*','*','*','*','*','3'],
          ['100','*','*','00:00:00:00:00:06','*','*','*','*','*','*','*','3'],

          ['100','*','*','00:00:00:00:00:07','*','*','*','*','*','*','*','4'],
          ['100','*','*','00:00:00:00:00:08','*','*','*','*','*','*','*','4'],
          ['100','*','*','00:00:00:00:00:09','*','*','*','*','*','*','*','4'],
          ['100','*','*','00:00:00:00:00:10','*','*','*','*','*','*','*','4'],
          ['100','*','*','00:00:00:00:00:11','*','*','*','*','*','*','*','4'],
          ['100','*','*','00:00:00:00:00:12','*','*','*','*','*','*','*','4'] ]

firewall_rules = [ ['100','0x0800','10.0.0.9', '10.0.0.1','6','80'],
                   ['100','0x0800','10.0.0.10','10.0.0.1','6','80'],
                   ['100','0x0800','10.0.0.11','10.0.0.1','6','80'],
                   ['100','0x0800','10.0.0.12','10.0.0.1','6','80'] ]

class FlowTable (EventMixin):
    
  def __init__ (self):
    self.listenTo(core.openflow)

  def _handle_ConnectionUp (self, event):
    ## DROP PACKETS ##
    for fr in firewall_rules:
      msg = of.ofp_flow_mod()
      if fr[0] != '*': msg.match.priority = int(fr[0])
      if fr[0] != '*': msg.match.dl_type  = int(fr[1], 16)
      if fr[0] != '*': msg.match.nw_src   = IPAddr(fr[2])
      if fr[0] != '*': msg.match.nw_dst   = IPAddr(fr[3])
      if fr[0] != '*': msg.match.nw_proto = int(6)
      if fr[0] != '*': msg.match.tp_dst   = int(80)
      event.connection.send(msg)
    ####

    ## ARP Request ##
    msg = of.ofp_flow_mod()
    msg.match.dl_type  = 0x0806
    msg.match.dl_dst = EthAddr('ff:ff:ff:ff:ff:ff')
    msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    event.connection.send(msg)
    ####

    ## Forwarding Rules ##
    for r in rules:
      msg = of.ofp_flow_mod()
      if r[0]  != '*':  msg.match.priority = int(r[0])#
      if r[1]  != '*':  msg.match.in_port  = int(r[1])#
      if r[2]  != '*':  msg.match.dl_src   = EthAddr(r[2])#
      if r[3]  != '*':  msg.match.dl_dst   = EthAddr(r[3])#
      if r[4]  != '*':  msg.match.dl_type  = int(r[4], 16)
      if r[5]  != '*':  msg.match.dl_vlan  = int(r[5])#
      if r[6]  != '*':  msg.match.nw_src   = IPAddr(r[6])
      if r[7]  != '*':  msg.match.nw_dst   = IPAddr(r[7])
      if r[8]  != '*':  msg.match.nw_proto = int(r[8])
      if r[9]  != '*':  msg.match.tp_src   = int(r[9])
      if r[10] != '*':  msg.match.tp_dst   = int(r[10])
      if r[11] != '*':  msg.actions.append(of.ofp_action_output(port = int(r[11])))
      event.connection.send(msg)
    ####

def launch ():
  core.registerNew(FlowTable)

