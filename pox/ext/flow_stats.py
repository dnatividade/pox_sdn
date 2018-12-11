#!/usr/bin/python
# Copyright 2012 William Yu
# wyu@ateneo.edu
#
# This file is part of POX.
#
# POX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# POX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with POX. If not, see <http://www.gnu.org/licenses/>.
#

"""
Adapted from original by:

Cairo Campos     <cairoapcampos@gmail.com>
Diego Natividade <natividade@bol.com.br>

"""

# standard includes
from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of

# include as part of the betta branch
from pox.openflow.of_json import *
from pox.lib.recoco import Timer
log = core.getLogger()

# handler for timer function that sends the requests to all the
# switches connected to the controller.
def _timer_func ():
	for connection in core.openflow._connections.values():
		connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
		connection.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))
	log.debug("Sent %i flow/port stats request(s)", len(core.openflow._connections))

# handler to display flow statistics received in JSON format
# structure of event.stats is defined by ofp_flow_stats()
def _handle_flowstats_received (event):
	stats = flow_stats_to_list(event.stats)
	log.debug("FlowStatsReceived from %s: %s", dpidToStr(event.connection.dpid), stats)
	file_status = open('status.txt', 'a+')
	stats = flow_stats_to_list(event.stats)
	#log.debug("PortStatsReceived from %s: %s", dpidToStr(event.connection.dpid), stats)
	##
	##log.debug("My code here...")
	'''
	for statistic in stats:
		string = '' 
		dic = statistic 
		for i, value in enumerate(dic.values()):
			##if i ==0 
			if i == len(dic)-1:
				string += str(value) + '\n'
			else:
				string += str(value) + ','
		log.debug('-> ' + string)
		file_status.write(string)
	file_status.close()
	#####################################################
	'''
	# Get number of bytes/packets in flows for web traffic only
	web_bytes = 0
	web_flows = 0
	web_packet = 0
	for f in event.stats:
		if f.match.tp_dst == 80 or f.match.tp_src == 80:
			web_bytes  += f.byte_count
			web_packet += f.packet_count
			web_flows  += 1
	log.info("Web traffic from %s: %s bytes (%s packets) over %s flows", dpidToStr(event.connection.dpid), web_bytes, web_packet, web_flows)

# handler to display port statistics received in JSON format
def _handle_portstats_received (event):
	file_status = open('status.txt', 'a+')
	stats = flow_stats_to_list(event.stats)
	#log.debug("PortStatsReceived from %s: %s", dpidToStr(event.connection.dpid), stats)
	##
	##log.debug("My code here...")
	for statistic in stats:
		string = '' 
		dic = statistic 
		for i, value in enumerate(dic.values()):
			##if i ==0 
			if i == len(dic)-1:
				string += str(value) + '\n'
			else:
				string += str(value) + ','
		log.debug('-> ' + string)
		file_status.write(string)
	#####################################################
	file_status.close()

    
# main functiont to launch the module
def launch ():
	#from pox.lib.recoco import *
	# attach handsers to listners
	core.openflow.addListenerByName("FlowStatsReceived", _handle_flowstats_received) 
	core.openflow.addListenerByName("PortStatsReceived", _handle_portstats_received) 

# timer set to execute every five seconds
Timer(5, _timer_func, recurring=True)

