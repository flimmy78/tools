#!/bin/sh
sed -i 's/NAME="em1"/NAME="eth0"/' /etc/udev/rules.d/70-persistent-net.rules
sed -i 's/NAME="em2"/NAME="eth1"/' /etc/udev/rules.d/70-persistent-net.rules
sed -i 's/NAME="em3"/NAME="eth2"/' /etc/udev/rules.d/70-persistent-net.rules
sed -i 's/NAME="em4"/NAME="eth3"/' /etc/udev/rules.d/70-persistent-net.rules

if [ -f /etc/sysconfig/network-scripts/ifcfg-em1 ]; then
    sed -i 's/DEVICE.*$/DEVICE=eth0/' /etc/sysconfig/network-scripts/ifcfg-em1
    mv /etc/sysconfig/network-scripts/ifcfg-em1 /etc/sysconfig/network-scripts/ifcfg-eth0
fi

if [ -f /etc/sysconfig/network-scripts/ifcfg-em2 ]; then
    sed -i 's/DEVICE.*$/DEVICE=eth1/' /etc/sysconfig/network-scripts/ifcfg-em2
    mv /etc/sysconfig/network-scripts/ifcfg-em2 /etc/sysconfig/network-scripts/ifcfg-eth1
fi

if [ -f /etc/sysconfig/network-scripts/ifcfg-em3 ]; then
    sed -i 's/DEVICE.*$/DEVICE=eth2/' /etc/sysconfig/network-scripts/ifcfg-em3
    mv /etc/sysconfig/network-scripts/ifcfg-em3 /etc/sysconfig/network-scripts/ifcfg-eth2
fi

if [ -f /etc/sysconfig/network-scripts/ifcfg-em4 ]; then
    sed -i 's/DEVICE.*$/DEVICE=eth3/' /etc/sysconfig/network-scripts/ifcfg-em4
    mv /etc/sysconfig/network-scripts/ifcfg-em4 /etc/sysconfig/network-scripts/ifcfg-eth3
fi

