#!/bin/bash
echo "-------------------"
echo "Loading SCENARIO 02"
echo "-------------------"
echo " "

POX6633="~/pox/pox.py  openflow.of_01 --port=6633  log.level --DEBUG  samples.pretty_log  s02_firewall_l3  forwarding.l3_learning --fakeways=10.10.0.254,10.20.0.254,10.30.0.254"

gnome-terminal -- bash -c "python2.7 $POX6633; $SHELL" &
sudo python2.7 trabalho-pratico/scenario02.py

exit 0

