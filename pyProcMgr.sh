#!/bin/bash

# Make sure we have procServ
source /reg/g/pcds/pkg_mgr/etc/add_env_pkg.sh  procServ/2.7.0-1.3.0
if [ ! -e "$(which procServ)" ]; then
	echo Error: procServ not found!
fi

# Make sure we have a canonical path to eco_tools
#this_script=`readlink -f $BASH_ARGV`
this_script=`readlink -f $0`
this_dir=`readlink -f $(dirname $this_script)`

$this_dir/pyProcMgr.py $*
