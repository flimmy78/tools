#!/bin/sh
install_path="/home/zhicloud/lib"



echo "loacl yum set ..."

cd /etc/yum.repos.d/
mv CentOS-Base.repo CentOS-Base.repo.bak
mv CentOS-Media.repo CentOS-Media.repo.bak
cp ${install_path}/CentOS-Media.repo .

cd ${install_path}
echo "install needs rpms"
yum install ${install_path}/rpm/*.rpm -y

mv /etc/yum.repos.d/CentOS-Base.repo.bak /etc/yum.repos.d/CentOS-Base.repo
mv /etc/yum.repos.d/CentOS-Media.repo.bak /etc/yum.repos.d/CentOS-Media.repo
echo "loacl yum reset"

