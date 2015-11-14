#!/bin/sh

cd /home/zhicloud
tar zxvf nc_img.tar.gz

free_mem=`free -m | awk 'NR==3 {print $4}'`
nc_mem=$[$free_mem*3/4*1000]
sed -i "s/<memory unit='KiB'>.*<\/memory>/<memory unit='KiB'>$nc_mem<\/memory>/" /home/zhicloud/nc_img/nc_aio.xml
sed -i "s/<currentMemory unit='KiB'>.*<\/currentMemory>/<currentMemory unit='KiB'>$nc_mem<\/currentMemory>/" /home/zhicloud/nc_img/nc_aio.xml

free_disk=$(df -h / | awk 'NR==2 {print substr($4, 0, length($4) - 1)}')
nc_disk=`awk -v free_disk="$free_disk" 'BEGIN{print free_disk*3/4}'`
qemu-img create -f raw /home/zhicloud/nc_img/sdbdisk.img ${nc_disk}G

virsh define nc_img/nc_aio.xml
virsh autostart nc_aio

