#!/bin/bash

PROCSERV=`which procServ`
if [ ! -e "$PROCSERV" ]; then
	echo "Error: procServ not found!"
	exit 1
fi

LOADSERVER=`which loadServer`
if [ ! -e "$LOADSERVER" ]; then
	echo "Error: loadServer not found!"
	exit 1
fi

PYPROCMGR_DIR=`readlink -f $(dirname ${BASH_SOURCE[0]})`
PYPROCMGR=$PYPROCMGR_DIR/pyProcMgr.py 
if [ ! -e "$PYPROCMGR" ]; then
	echo "Error: pyProcMgr.py not found!"
	exit 1
fi
echo PYPROCMGR = $PYPROCMGR_DIR 

TOP=`readlink -f $(dirname $LOADSERVER)/../..`
echo TOP = $TOP

cd $TOP
$PYPROCMGR -c 10 $LOADSERVER \
	'-m DELAY=0.010,P=PVA:GW:TEST:$PYPROC_ID:,NELM=10'	\
	'-d db/drive_100Counters.db'

#$LOADSERVER	\
#	-m DELAY=1.0,P=PVA:GW:TEST:1:,NELM=10	\
#	-d $TOP/db/drive_10Counters.db


