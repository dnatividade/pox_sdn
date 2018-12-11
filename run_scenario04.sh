#!/bin/bash
echo "-------------------"
echo "Loading SCENARIO 04"
echo "-------------------"
echo " "

POX6631="~/pox/pox.py  openflow.of_01 --port=6631  log.level --DEBUG  samples.pretty_log  s04_flow_table_c1  s04_firewall_l3"
POX6632="~/pox/pox.py  openflow.of_01 --port=6632  log.level --DEBUG  samples.pretty_log  s04_flow_table_c2  s04_firewall_l3"
POX6633="~/pox/pox.py  openflow.of_01 --port=6633  log.level --DEBUG  samples.pretty_log  s04_flow_table_c3  s04_firewall_l3"

gnome-terminal -- bash -c "python2.7 $POX6631; $SHELL" &
gnome-terminal -- bash -c "python2.7 $POX6632; $SHELL" &
gnome-terminal -- bash -c "python2.7 $POX6633; $SHELL" &

sudo python2.7 trabalho-pratico/scenario04.py

exit 0

