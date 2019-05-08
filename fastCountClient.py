#!/bin/env python3

import argparse
import logging
import sys
import textwrap
import time

from functools import partial
from p4p.client.thread import Context
from p4p.client.raw import Disconnected, RemoteError, Cancelled, Finished, LazyRepr
from threading import Lock

_log	= logging.getLogger(__name__)
_ctxt	= Context('pva')

class fastCountClient(object):
    def __init__( self ):
        self._ctxt = Context('pva')
        self._lock = Lock()
        self._subscriptions = {}

    def callback( self, pvName, cbData ):
        if isinstance( cbData, (RemoteError, Disconnected, Cancelled)):
            print( '%s: %s' % ( pvName, cbData ) )
            return

        pvaValue = cbData
        print( '%s: New value = %s' % ( pvName, pvaValue ) )
        #print( '%s: New value fields %s' % ( pvName, dir(pvaValue) ) )
        print( '%s: value timestamp = %s' % ( pvName, pvaValue.timestamp ) )
        print( '%s: value raw_stamp = %s' % ( pvName, pvaValue.raw_stamp ) )
        print( '%s: value status = %s' % ( pvName, pvaValue.status ) )
        print( '%s: value severity = %s' % ( pvName, pvaValue.severity ) )
        print( '%s: value.is_integer() = %s' % ( pvName, pvaValue.is_integer() ) )
        print( '%s: value __class__ = %s' % ( pvName, pvaValue.__class__ ) )
        print( '%s: value real = %s' % ( pvName, pvaValue.real ) )
        print( '%s: value imag = %s' % ( pvName, pvaValue.imag ) )
        print( '%s: value hex = %s' % ( pvName, pvaValue.hex ) )
        print( '%s: value fromhex = %s' % ( pvName, pvaValue.fromhex ) )
        print( '%s: value conjugate = %s' % ( pvName, pvaValue.conjugate ) )

    def monitorPvs( self, pvNames ):
        for pvName in pvNames:
            self._subscriptions[ pvName ] = self._ctxt.monitor( pvName, partial( self.callback, pvName ), notify_disconnect=True )

    def closeSubscriptions( self ):
        for S in self._subscriptions.values():
            print( "Closing subscription to %s" % S.name )
        [S.close() for S in self._subscriptions.values()]

    def __exit__( self ):
        self.closeSubscriptions()

def process_options(argv):
    if argv is None:
        argv = sys.argv[1:]
    description = 'epics-build builds one or EPICS module releases.\n'
    epilog_fmt = '\nStandard EPICS modules can be specified w/ just the module basename.\n'\
            + '\nExamples:\n' \
            + 'epics-build -p asyn/4.31-0.1.0 --top /afs/slac/g/lcls/epics/R3.15.5-1.0/modules\n'
    epilog = textwrap.dedent( epilog_fmt )
    parser = argparse.ArgumentParser( description=description, formatter_class=argparse.RawDescriptionHelpFormatter, epilog=epilog )
    parser.add_argument( '-p', '--pvName',   dest='pvNames', action='append', \
                        help='EPICS PVA pvNames Example: TEST:01:AnalogIn0', default=[] )
#   parser.add_argument( '-b', '--base',     action='store',  help='Use to set EPICS_BASE in RELEASE_SITE' )
    parser.add_argument( '-f', '--input_file_path', action='store', help='Read list of pvNames from this file' )
    parser.add_argument( '-v', '--verbose',  action="store_true", help='show more verbose output.' )

    options = parser.parse_args( )

    return options 

def main(argv=None):
    options = process_options(argv)

    pvNames = [ 'PVA:GW:TEST:1:Rate', 'PVA:GW:TEST:2:Rate', 'PVA:GW:TEST:3:Rate' ]
    fc = fastCountClient()
    fc.monitorPvs( pvNames )

    time.sleep(10)
    fc.closeSubscriptions()
    time.sleep(1)

if __name__ == '__main__':
    status = main()
    sys.exit(status)
