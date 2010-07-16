#!/bin/sh
while true; do
    sleep 600
#    [ ! -e "/home/yanchuan/download/fhx.pl-{c98d4339-1dfe-437b-be61-bf583ccebb6a}.dtapart" ] && sudo shutdown -h now
#    [ ! -d /tmp/virtual-yc.2P1lk7 ] && sudo shutdown -h now
    a=`date +%H`
    [ $a -gt 5 -a $a -lt 17 ] && sudo shutdown -h now
done
