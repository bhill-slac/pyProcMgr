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
TOP=`readlink -f $(dirname $LOADSERVER)/../..`
echo PYPROCMGR_DIR = $PYPROCMGR_DIR 
echo TOP = $TOP

cd $TOP
#$PYPROCMGR_DIR/pyProcMgr.py -c 10 $LOADSERVER	\
#	"-m 'DELAY=1.0,P=PVA:GW:TEST:$PYPROC_ID:,NELM=10'"	\
#	"-d $TOP/db/drive_10Counters.db"
$LOADSERVER	\
	"-m 'DELAY=1.0,P=PVA:GW:TEST:$PYPROC_ID:,NELM=10'"	\
	"-d $TOP/db/drive_10Counters.db"

