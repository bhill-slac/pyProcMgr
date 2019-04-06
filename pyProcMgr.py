#!/usr/bin/env python
#  Name: pyProcMgr.py
#  Abs:  A python tool to launch and manage processes
#
#  Example:
#    pyProcMgr --cmd "echo hello world"
#
#  Requested features to be added:
#
#==============================================================
import sys
import os
#import socket
import subprocess
import argparse
#import readline
#import shutil
#import tempfile
#import textwrap

def process_options(argv):
    if argv is None:
        argv = sys.argv[1:]
    description =	'pyProcMgr supports ...\n'
    epilog_fmt  =	'\nExamples:\n' \
                    'pyProcMgr --foo\n'
    epilog = textwrap.dedent( epilog_fmt )
    parser = argparse.ArgumentParser( description=description, formatter_class=argparse.RawDescriptionHelpFormatter, epilog=epilog )
    parser.add_argument( '-p', '--package',   dest='packages', action='append', \
                        help='EPICS module-name/release-version. Ex: asyn/R4.30-1.0.1', default=[] )
    parser.add_argument( '-f', '--input_file_path', action='store', help='Read list of module releases from this file' )
    parser.add_argument( '-v', '--verbose',  action="store_true", help='show more verbose output.' )
    parser.add_argument( '--version',  		 action="version", version=eco_tools_version )

    options = parser.parse_args( )

    return options 

def main(argv=None):
    options = process_options(argv)

    print "Done:"
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)
