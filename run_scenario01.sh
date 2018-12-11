#!/bin/bash
echo "-------------------"
echo "Loading SCENARIO 01"
echo "-------------------"
echo " "

#POX6633="~/pox/pox.py  openflow.of_01 --port=6633  log.level --DEBUG  samples.pretty_log  forwarding.l2_learning  s01_firewall_l2"
POX6633="~/pox/pox.py  openflow.of_01 --port=6633  log.level --DEBUG  samples.pretty_log  forwarding.l2_learning s01_firewall_l2"

gnome-terminal -- bash -c "python2.7 $POX6633; $SHELL" &
sudo python2.7 trabalho-pratico/scenario01.py

exit 0

