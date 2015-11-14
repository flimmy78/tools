#!/bin/sh

if [ $# -lt 2 ]; then
        echo "you need give 2 param,param1:iso base dectionary,isoname,param2:the zhicloud install dectionary"
        exit -1
fi

sed -i $1 $2
