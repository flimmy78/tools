#!/bin/sh

cp /etc/sysconfig/network-scripts/ifcfg-eth0 /etc/sysconfig/network-scripts/ifcfg-br0
sed -i '/BRIDGE.*/d' /etc/sysconfig/network-scripts/ifcfg-eth0
echo "BRIDGE=br0" >> /etc/sysconfig/network-scripts/ifcfg-eth0
sed -i 's/DEVICE.*/DEVICE=br0/' /etc/sysconfig/network-scripts/ifcfg-br0
sed -i 's/TYPE.*/TYPE=Bridge/' /etc/sysconfig/network-scripts/ifcfg-br0

