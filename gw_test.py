#!/bin/env python3

from p4p.client.thread import Context

ctxt = Context('pva')

pvName = 'PVA:GW:TEST:1:iq' 
iq = ctxt.get( pvName )

print( '%s:' % pvName, iq )


def callback( pvaValue ):
    #print( 'New value:', pvaValue )
    print( 'New value changed:', pvaValue.changedSet() )
    if 'Q.alarm.message' in pvaValue.changedSet():
        print( 'Q.alarm.message: %s' % pvaValue['Q.alarm.message'] )
        print( 'I.alarm: %s' % pvaValue['I.alarm'] )

subscription = ctxt.monitor( pvName, callback )

import time
time.sleep(100)

subscription.close()

