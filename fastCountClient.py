#!/bin/env python3

import argparse
import logging
import json
import os
import sys
import textwrap
import time

#from functools import partial
from p4p.client.thread import Context
from p4p.client.raw import Disconnected, RemoteError, Cancelled, Finished, LazyRepr
from threading import Lock
import p4p.nt.scalar

_log	= logging.getLogger(__name__)
_ctxt	= Context('pva')

class fastCountClient(object):
    def __init__( self, pvName, verbose=False ):
        self._lock = Lock()
        self._pvName = pvName
        self._history = []
        self._priorValue = None
        self._verbose = verbose
        self._S = _ctxt.monitor( pvName, self.callback, notify_disconnect=True )

    def pvName( self ):
        return self._pvName

    def callback( self, cbData ):
        pvName = self._pvName
        if isinstance( cbData, (RemoteError, Disconnected, Cancelled)):
            print( '%s: %s' % ( pvName, cbData ) )
            return

        pvaValue = cbData

        if self._priorValue is not None:
            # Check for missed count
            expectedValue = self._priorValue + 1
            if expectedValue != pvaValue:
                print( '%s: missed %d counts!' % ( pvName, pvaValue - expectedValue ) )

        self._priorValue	= pvaValue
        self._history.append((pvaValue.raw_stamp,pvaValue))
        if isinstance( pvaValue, p4p.nt.scalar.ntfloat ):
            self._priorCount = int(pvaValue)

        if self._verbose:
            print( '%s: New value = %s' % ( pvName, pvaValue ) )
            print( '%s: Num values = %d' % ( pvName, len(self._history)) )
            #print( '%s: New value fields %s' % ( pvName, dir(pvaValue) ) )
            print( '%s: value timestamp = %s' % ( pvName, pvaValue.timestamp ) )
            print( '%s: value raw_stamp = %s' % ( pvName, pvaValue.raw_stamp ) )
            #print( '%s: value status = %s' % ( pvName, pvaValue.status ) )
            #print( '%s: value severity = %s' % ( pvName, pvaValue.severity ) )
            #print( '%s: value __class__ = %s' % ( pvName, pvaValue.__class__ ) )
            if isinstance( pvaValue, p4p.nt.scalar.ntfloat ):
                print( '%s: value real = %s' % ( pvName, pvaValue.real ) )
                #print( '%s: value imag = %s' % ( pvName, pvaValue.imag ) )
                #print( '%s: value.is_integer() = %s' % ( pvName, pvaValue.is_integer() ) )
                #print( '%s: value hex = %s' % ( pvName, pvaValue.hex ) )
                #print( '%s: value fromhex = %s' % ( pvName, pvaValue.fromhex ) )
                #print( '%s: value conjugate = %s' % ( pvName, pvaValue.conjugate ) )

    def saveValues( self, dirName ):
        if not os.path.isdir( dirName ):
            os.mkdir( dirName )
        saveFile = os.path.join( dirName, self._pvName )
        try:
            with open( saveFile, "w" ) as f:
                print( "Saving %d values to %s ..." % ( len(self._history), saveFile ) )
                json.dump( self._history, f, indent=4 )
                #for v in self._history:
                #	f.write( "%f, %d\n" % ( v.timestamp, v.real ) )
        except:
            print( "Unable to save values to %s" % saveFile )

    def closeSubscription( self ):
        if self._S is not None:
            print( "Closing subscription to %s" % self._pvName )
            self._S.close()
            self._S = None

    def __exit__( self ):
        self.closeSubscription()

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

    pvNames = [ 'PVA:GW:TEST:1:Count', 'PVA:GW:TEST:2:Count', 'PVA:GW:TEST:3:Count' ]
    #pvNames = [ 'PVA:GW:TEST:1:Rate', 'PVA:GW:TEST:2:Rate', 'PVA:GW:TEST:3:Rate' ]
    clients = []
    #pvaValue = _ctxt.get( pvNames[0] )
    for pvName in pvNames:
        clients.append( fastCountClient( pvName, options.verbose ) )

    try:
        time.sleep(5)
    except KeyboardInterrupt:
        pass
    for client in clients:
        client.closeSubscription()
    for client in clients:
        client.saveValues('/tmp/fastClient')
    time.sleep(1)

if __name__ == '__main__':
    status = main()
    sys.exit(status)
