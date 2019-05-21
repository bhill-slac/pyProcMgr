#!/bin/bash

PROCSERV=`which procServ`
if [ ! -e "$PROCSERV" ]; then
	echo "Error: procServ not found!"
	exit 1
fi

SOFTIOCPVA=`which softIocPVA`
if [ ! -e "$SOFTIOCPVA" ]; then
	echo "Error: softIocPVA not found!"
	exit 1
fi

./pyProcMgr.py -c 5 $SOFTIOCPVA '-m P=PVA:GW:TEST:$PYPROC_ID:,NELM=100000,N=0' '-d fastCount.db'
