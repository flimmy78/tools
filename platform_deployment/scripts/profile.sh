#!/bin/sh

if [ -x /usr/bin/id ]; then
    if [ -z "$EUID" ]; then
        # ksh workaround
        EUID=`id -u`
        UID=`id -ru`
    fi
    USER="`id -un`"
    LOGNAME=$USER
    MAIL="/var/spool/mail/$USER"
fi
#sh /etc/profile.d/colorls.sh
sh /etc/profile.d/cvs.sh
sh /etc/profile.d/glib2.sh

#sh /etc/profile.d/less.sh
#sh /etc/profile.d/vim.sh
#sh /etc/profile.d/which2.sh






