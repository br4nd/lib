#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
read_log(ffn_in)
returns all data in dictionary D
"""

import pdb
import os, sys
import numpy as np
import numpy.lib.recfunctions
import pprint as pp
from parse_msg import parse_msg

D = dict()
def read_log(ffn_in) :

    if not os.path.isfile(ffn_in) :
        print 'First argument must be the full file name of the log file'
        return([])


    with open(ffn_in,'r') as f:
        iline = 0

        D['NodeIDs'] = []
        for line in f:
            iline += 1
            if not iline % 500 : # print a line once in a while
                print '%d: %s' % (iline,line[0:99].strip('\n'))

            msg = parse_msg(line)
            if not msg : # msg is empty
                continue

            # Get rid of blank lines
            if len(line) < 5 :
                continue

            if 'RcmConfig' == msg['msgType'] :
                D['RcmConfig'] = msg
                thisNodeId = msg['NodeID']
                if thisNodeId not in D['NodeIDs'] :
                    D['NodeIDs'].append(thisNodeId)

            elif 'RcmRangeInfo' == msg['msgType'] :
                msg['RequesterID'] = thisNodeId

                if msg['ResponderID'] not in D['NodeIDs'] :
                    D['NodeIDs'].append(msg['ResponderID'])

                rangeArray = process_rcm_msg(msg)
                if not 'RcmRanges' in D :
                    D['RcmRanges'] = rangeArray
                else :
                    D['RcmRanges'] = np.vstack((D['RcmRanges'],rangeArray))

            elif 'RcmEchoedRangeInfo' == msg['msgType'] :

                if msg['RequesterID'] not in D['NodeIDs'] :
                    D['NodeIDs'].append(msg['RequesterID'])

                if msg['ResponderID'] not in D['NodeIDs'] :
                    D['NodeIDs'].append(msg['ResponderID'])

                rangeArray = process_echoed_range_info(msg)

                if not 'RcmEchoedRanges' in D :
                    D['RcmEchoedRanges'] = rangeArray
                else :
                    D['RcmEchoedRanges'] = np.vstack((D['RcmEchoedRanges'],rangeArray))

            elif 'RcmScanInfo' == msg['msgType'] :
                print 'SKIPPED RcmScanInfo'
#                D['RcmScanArray']['LinkID'] = D['RcmScanArray'].append(np.array(msg['ScanData'])/1000.)

            elif 'MrmConfig' == msg['msgType'] :
                D['MrmConfig'] = msg

            elif 'MrmControlRequest' == msg['msgType'] :
                D['MrmControlRequest'] = msg

            elif 'MrmFullScanInfo' == msg['msgType'] :
                if msg['Filtering'] == 1 :
                    if 'MrmScanRawArray' not in D.keys() :
                        D['MrmScanRawTimes'] = np.array(msg['Timestamp'])
                        D['MrmScanRawArray'] = msg['ScanData']
                    else :
                        D['MrmScanRawTimes'] = np.append(D['MrmScanRawTimes'],msg['Timestamp'])
                        D['MrmScanRawArray'] = np.vstack((msg['ScanData'],D['MrmScanRawArray']))

            pass

    return D

def process_rcm_msg(msg) :
    #pdb.set_trace()
    msgType = msg['msgType']
    msgID = msg['MessageID']
    reqID = msg['RequesterID']
    rspID = msg['ResponderID']
    t_host = msg['Timestamp']
    t_embedded = msg['EmbeddedTimestamp']
    vpeak = msg['Vpeak']
    noise = msg['Noise']
    ledflags = msg['ReqLEDFlags'] | msg['RespLEDFlags']
    t_stopwatch = msg['StopwatchTime']
    status = msg['RangeStatus']
    ree = msg['PrecisionRangeErrEst']
    rmeas = msg['PrecisionRange']
    reqAntMode = msg['ReqAntennaMode']
    rspAntMode = msg['RespAntennaMode']

    # Support new reqSNR which is labeled 'Reserved'
    if 'Reserved' in msg.keys() :
        reqSNR = msg['Reserved']
        rangeArray = np.array([(msgType,msgID,reqID,rspID,t_host,t_embedded,vpeak,
            noise,ledflags,t_stopwatch,status,ree,rmeas,reqAntMode,rspAntMode,reqSNR)],
            dtype= [('msgType','S20'),
                    ('msgID','i4'),
                    ('reqID','i4'),
                    ('rspID','i4'),
                    ('t_host','<f8'),
                    ('t_embedded','<f8'),
                    ('vpeak','<f4'),
                    ('noise','<f4'),
                    ('ledflags','i4'),
                    ('t_stopwatch','i4'),
                    ('status','i4'),
                    ('ree','<f4'),
                    ('rmeas','<f4'),
                    ('reqAntMode','i4'),
                    ('rspAntMode','i4'),
                    ('reqSNR','i4'),
                ])

    else :  # old - easier than adding a new element to a structured array
        rangeArray = np.array([(msgType,msgID,reqID,rspID,t_host,t_embedded,vpeak,
            noise,ledflags,t_stopwatch,status,ree,rmeas,reqAntMode,rspAntMode)],
            dtype= [('msgType','S20'),
                    ('msgID','i4'),
                    ('reqID','i4'),
                    ('rspID','i4'),
                    ('t_host','<f8'),
                    ('t_embedded','<f8'),
                    ('vpeak','<f4'),
                    ('noise','<f4'),
                    ('ledflags','i4'),
                    ('t_stopwatch','i4'),
                    ('status','i4'),
                    ('ree','<f4'),
                    ('rmeas','<f4'),
                    ('reqAntMode','i4'),
                    ('rspAntMode','i4'),
                ])

    return rangeArray

def process_echoed_range_info(msg) :
    msgType = msg['msgType']
    msgID = msg['MessageID']
    reqID = msg['RequesterID']
    rspID = msg['ResponderID']
    t_host = msg['Timestamp']
    t_embedded = msg['EmbeddedTimestamp']
    ledflags = msg['LEDFlags']
    ree = msg['PrecisionRangeErrEst']
    rmeas = msg['PrecisionRange']
    rangeArray = np.array([(msgType,msgID,reqID,rspID,t_host,t_embedded,
        ledflags,ree,rmeas)],
                    dtype= [('msgType','S20'),
                            ('msgID','i4'),
                            ('reqID','i4'),
                            ('rspID','i4'),
                            ('t_host','<f8'),
                            ('t_embedded','<f8'),
                            ('ledflags','i4'),
                            ('ree','<f4'),
                            ('rmeas','<f4'),
                        ])
    return rangeArray
