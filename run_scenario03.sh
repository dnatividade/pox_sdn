#!/bin/bash
echo "-------------------"
echo "Loading SCENARIO 03"
echo "-------------------"
echo " "

POX6633="~/pox/pox.py  openflow.of_01 --port=6633  log.level --DEBUG  samples.pretty_log  forwarding.l3_learning  s03_firewall_l3"

gnome-terminal -- bash -c "python2.7 $POX6633; $SHELL" &
sudo python2.7 trabalho-pratico/scenario03.py

exit 0

