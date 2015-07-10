#!/bin/sh
install_path="/home/zhicloud/lib"
ipsutil=0
ilibvirt=0
iglib=0
inbd=0
itftp=0
ikenelreplace=0

if [ ! -d /usr/local/zhicloud ] 
then
mkdir /usr/local/zhicloud
fi

if [ ! -f /usr/local/zhicloud/zhicloud.conf ] 
then
cp -f /home/zhicloud/lib/zhicloud.conf /usr/local/zhicloud/zhicloud.conf
fi

if echo "$*" | grep -q "data_server" 
then
sed -i '/data_server.*$/d' /usr/local/zhicloud/zhicloud.conf
echo "data_server=enable" >> /usr/local/zhicloud/zhicloud.conf

fi

if echo "$*" | grep -q "control_server" 
then
sed -i '/control_server.*$/d' /usr/local/zhicloud/zhicloud.conf
echo "control_server=enable" >> /usr/local/zhicloud/zhicloud.conf


fi

if echo "$*" | grep -q "statistic_server" 
then
sed -i '/statistic_server.*$/d' /usr/local/zhicloud/zhicloud.conf
echo "statistic_server=enable" >> /usr/local/zhicloud/zhicloud.conf

fi

if echo "$*" | grep -q "storage_server" 
then
sed -i '/storage_server.*$/d' /usr/local/zhicloud/zhicloud.conf
echo "storage_server=enable" >> /usr/local/zhicloud/zhicloud.conf

iglib=1
inbd=1
itftp=1
fi

if echo "$*" | grep -q "node_client" 
then
sed -i '/node_client.*$/d' /usr/local/zhicloud/zhicloud.conf
echo "node_client=enable" >> /usr/local/zhicloud/zhicloud.conf

ipsutil=1
ilibvirt=1
iglib=1
inbd=1
ikenelreplace=1
fi

sed -i '/zhicloud\/autostart.*$/d' /etc/rc.d/rc.local
echo "python /usr/local/zhicloud/autostart.py" >> /etc/rc.d/rc.local

cp -f /home/zhicloud/lib/autostart.py /usr/local/zhicloud/autostart.py

echo "loacl yum set ..."


cd /etc/yum.repos.d/
mv CentOS-Base.repo CentOS-Base.repo.bak
mv CentOS-Media.repo CentOS-Media.repo.bak
cp ${install_path}/CentOS-Media.repo .

cd ${install_path}
echo "install needs rpms"
yum install ${install_path}/rpm/*.rpm -y
echo "install protobuf"
tar -zxf protobuf-2.5.0.tar.gz
cd protobuf-2.5.0
./configure&&make&&make check&&make install
mv ${install_path}/setuptools-0.6c11-py2.6.egg ${install_path}/protobuf-2.5.0/python
cd python
python ./setup.py build
python ./setup.py test
python ./setup.py install


echo "export PYTHONPATH=/home/zhicloud/shared:$PYTHONPATH" >> ~/.bashrc

if [ $ipsutil -eq 1 ];
then
echo "start install psutil..."

cd ${install_path}/
tar -zxf psutil-1.0.1.tar.gz
cd psutil-1.0.1
python ./setup.py install

echo "completed install psutil..."

fi

if [ $ilibvirt -eq 1 ];
then
echo "start install qemu&libvirt..."
chkconfig cgconfig on
service cgconfig start


echo "start config vnc&qemu..."

sed -i 's/#vnc_listen = "0.0.0.0"/vnc_listen = "0.0.0.0"/g' /etc/libvirt/qemu.conf
echo "set config vnc_listen = 0.0.0.0"
sed -i 's/#user = "root"/user = "root"/g' /etc/libvirt/qemu.conf
echo "set config user = root"
sed -i 's/#group = "root"/group = "root"/g' /etc/libvirt/qemu.conf
echo "set config group = root"
echo "start service libvirtd..."
service libvirtd start
fi

if [ $iglib -eq 1 ];
then
echo "start Install nbd client.."
echo "start Install autoconf 2.56.."

cd ${install_path}
tar -zxf autoconf-2.69.tar.gz
cd autoconf-2.69
./configure --prefix=/usr&&make&&make install

echo "start Install automake 1.13.."
cd ${install_path}
tar xJf automake-1.13.4.tar.xz
cd automake-1.13.4
./configure --prefix=/usr&&make&&make install

echo "update Install glib to 2.36.4"

cd ${install_path}
tar xJf glib-2.36.4.tar.xz
cd glib-2.36.4
./configure --prefix=/usr&&make&&make install

cp ${install_path}/glib-2.0.pc /usr/lib64/pkgconfig/.


echo "check glib version"
pkg-config --modversion glib-2.0

echo "rebuild X64 System lib link"

rm -f /lib64/libglib-2.0.so.0
ln -s /usr/lib/libglib-2.0.so.0.3600.4 /lib64/libglib-2.0.so.0
fi

if [ $inbd -eq 1 ];
then
echo "build nbd"
cd ${install_path}
tar jxf nbd-3.3.tar.bz2
cd nbd-3.3
./configure&&make&&make install
fi

if [ $ikenelreplace -eq 1];
then
yum install kernel-devel kernel-headers -y
yum install -y rpm-build redhat-rpm-config asciidoc hmaccalc perl-ExtUtils-Embed xmlto
yum install -y binutils-devel elfutils-libelf-devel newt-devel python-devel zlib-devel
yum install -y patchutils bison rng-tools 
yum install -y rpm-build redhat-rpm-config unifdef

mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

echo "%_topdir %(echo $HOME)/rpmbuild" > ~/.rpmmacros

rngd -r /dev/urandom


cd ${install_path}
rpm -i kernel-2.6.32-358.18.1.el6.src.rpm
cd ~/rpmbuild/SPECS
rpmbuild -bp --target=$(uname -m) kernel.spec
cd ~/rpmbuild/SOURCES
tar jxf linux-2.6.32-358.18.1.el6.tar.bz2 -C /usr/src/kernels/
cd /usr/src/kernels/
mv 2.6.32-358.23.2.el6.x86_64/ $(uname -r)-old
mv linux-2.6.32-358.18.1.el6/ $(uname -r)
cd $(uname -r)
make mrproper
cp ../$(uname -r)-old/Module.symvers ./
cp /boot/config-$(uname -r) ./.config
make oldconfig
make prepare
make scripts
make CONFIG_BLK_DEV_NBD=m M=drivers/block
cd /usr/src/kernels/$(uname -r)
cp drivers/block/nbd.ko /lib/modules/$(uname -r)/kernel/drivers/block/
depmod -a
modprobe nbd
lsmod|grep nbd
fi

if [ $itftp -eq 1 ];
then
echo "config tftp server..."
mv /etc/xinetd.d/tftp /etc/xinetd.d/tftp.bck
cp ${install_path}/tftp /etc/xinetd.d/tftp
service xinetd restart
fi

echo "config communication"
iptables -I INPUT -m state --state NEW -p udp --dport 5600:5799 -j ACCEPT
iptables -I INPUT -m state --state NEW -p tcp --dport 5900:5950 -j ACCEPT
iptables -I INPUT -m state --state NEW -p tcp --dport 10809 -j ACCEPT
service iptables save


echo "reset sys config"

cat /home/zhicloud/rc.local.cache > /etc/rc.d/rc.local
echo "modprobe nbd" >> /etc/rc.d/rc.local
mv /etc/yum.repos.d/CentOS-Base.repo.bak /etc/yum.repos.d/CentOS-Base.repo
mv /etc/yum.repos.d/CentOS-Media.repo.bak /etc/yum.repos.d/CentOS-Media.repo
echo "loacl yum reset"


echo "#############################################################"
echo "################service install completed!###################"
echo "#############################################################"

export PYTHONPATH=/home/zhicloud/shared:$PYTHONPATH

sed -i '/zhicloud\/autostart.*$/d' /etc/rc.d/rc.local
echo "python /usr/local/zhicloud/autostart.py" /etc/rc.d/rc.local

cp -f /home/zhicloud/lib/autostart.py /usr/local/zhicloud/autostart.py

python /usr/local/zhicloud/autostart.py
