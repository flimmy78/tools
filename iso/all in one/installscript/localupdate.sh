#!/bin/sh
if [ $# -lt 3 ]; then
        echo "you need give 2 param,param1:iso base dectionary,isoname,param2:the zhicloud install dectionary"
        exit -1
fi

sed -i $1 $3
echo $2 >> $3
