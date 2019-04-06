#!/bin/bash

# Make sure we have a canonical path to eco_tools
this_script=`readlink -f $BASH_ARGV`
this_dir=`readlink -f $(dirname $this_script)`

$this_dir/pyProcMgr.py $*
