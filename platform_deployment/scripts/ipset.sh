#/bin/bash
 read   -p "do you want to configure nework[Y/N]?" reply 
case $reply in
 Y|y)
 echo
 echo "***************************************" 
 echo "--------network configuration----------"
echo
 sed -i 's/BOOTPROTO.*$/BOOTPROTO=static/g' /etc/sysconfig/network-scripts/ifcfg-eth0  
 while true
 do
 read -p "please input IP:" IP
 echo ${IP}
 if echo $IP|grep "^[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}$"  
then
 sed -i '/IPADDR.*$/d' /etc/sysconfig/network-scripts/ifcfg-eth0
 
 echo "IPADDR="${IP} >> /etc/sysconfig/network-scripts/ifcfg-eth0
 
 break
 else
 echo "please check IP format..."
 fi
 done

 read -p "please input netmask:" NETMASK
 sed -i '/NETMASK.*$/d' /etc/sysconfig/network-scripts/ifcfg-eth0
 
 echo "NETMASK="$NETMASK >> /etc/sysconfig/network-scripts/ifcfg-eth0
 
 while true
 do
 read -p "please input gateway:" GATEWAY
 
 sed -i '/GATEWAY.*$/d' /etc/sysconfig/network-scripts/ifcfg-eth0
 
 echo "GATEWAY="$GATEWAY >> /etc/sysconfig/network-scripts/ifcfg-eth0

 echo "please check gateway format..."
 break
 done 

 while true
 do
 read -p "please input DNS:" DNS
 if  echo $DNS|grep "^[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}$"
 then
 DNS=`echo nameserver $DNS`  
 echo $DNS >>/etc/resolv.conf
 break
 else
 echo "please check DNS format..."
 fi
 done
 ifconfig eth0 up 
/etc/rc.d/init.d/network restart
mentohust=`whereis mentohust` 
 if [ mentohust="mentohust:" ] 
then
 echo "there is no mentohust...."
 else
 mentohust & 
fi
 TEMP=`mktemp -t temp.XXXXXX`
 echo $TEMP
 echo "Testing Network......"  
exec 2>$TEMP
 `echo ping -c 5 $GATEWAY` >>$TEMP
 if  grep "unknown host"  $TEMP   
 then
 echo "network timeout,please check network configuration"
 else
 echo
 echo "*******************************************"
 echo "OK,good luck!" 
 fi
 sed -i 's/ip = 0.0.0.0/ip = '${IP}'/g' /home/zhicloud/data_server/node.conf
 rm -rf $TEMP;;
 N|n)  
 exit;;
 esac
