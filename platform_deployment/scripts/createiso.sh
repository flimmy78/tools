#!/bin/sh

if [ $# -lt 3 ]; then
	echo "you need give 2 param,param1:iso base dectionary,isoname,param2:the zhicloud install dectionary"
	exit -1
fi

cp -r "$1" disk_temp
disk_path="$(pwd)/disk_temp" 

zhicloud_path="$2"
isoname="$3"

echo -e "cd ${disk_path}"

cd ${disk_path}

echo -e "cp  ${zhicloud_path}  to ${disk_path}"

cp -rf ${zhicloud_path} zhicloud

echo "createrepo..."

createrepo -g ${disk_path}/repo_comps.xml ${disk_path}/

cd ..

mkisofs -R -J -T -v -no-emul-boot -boot-load-size 4 -boot-info-table -V RHEL4ASDVD -b isolinux/isolinux.bin -c isolinux/boot.cat -o ${isoname} /${disk_path}

rm -rf ${disk_path}
