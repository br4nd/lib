#!/usr/local/bin/python
import pdb
import os, sys
import numpy as np

def parse_msg(msg_in) :

    msglist = msg_in.split(",")

    if len(msg_in) < 3 :
        return []

    if 'Timestamp' == msglist[0]: # jump over msg descriptions
        return []

    elif ' RcmGetStatusInfoConfirm' == msglist[1] :
        #Timestamp, RcmGetStatusInfoConfirm, MessageID, PackageID, RcmVersion, UwbKernelVersion, FpgaVersion, SerialNumber, BoardType, PulserConfig, BITResults, Temperature(degC), Status
        #1444064949.000, RcmGetStatusInfoConfirm, 0, NN-dev-4 Oct  2 2015 18:38:36RL, 0.2.6, 2.2.51420, [2001.01.01] Rev 1, DEADBEEF, P330 Rev A, FCC, 0, 33.75, 0
        msg = dict([('msgType','RcmGetStatusInfoConfirm'),
                    ('Timestamp',float(msglist[0])),
                    ('MessageID',int(msglist[2])),
                    ('PackageID',msglist[3][1:]),
                    ('RcmVersion',msglist[4][1:]),
                    ('UwbKernelVersion',msglist[5][1:]),
                    ('FpgaVersion',msglist[6][1:]),
                    ('SerialNumber',msglist[7][1:]),
                    ('BoardType',msglist[8][1:]),
                    ('PulserConfig',msglist[9][1:]),
                    ('BITResults',int(msglist[10])),
                    ('temperature',float(msglist[11])),
                    ('Status',int(msglist[12]))
                    ])
        return msg

    elif ' RcmConfig' == msglist[1] :
        #Timestamp, RcmConfig, NodeId, PulseIntegrationIndex, AntennaMode, AntennaToggleFlag, CodeChannel, AntennaDelayA, AntennaDelayB, ScanInfo, DisableCRERanges, TransmitGain, ELR
        #1444409248.067, RcmConfig, 112, 7, 1, False, 5, 0, 0, 0, True, 63, False
        msg = dict([('msgType','RcmConfig'),
                    ('Timestamp',float(msglist[0])),
                    ('NodeID',int(msglist[2])),
                    ('PulseIntegrationIndex',int(msglist[3])),
                    ('AntennaMode',int(msglist[4])),
                    ('AntennaToggleFlag',bool(msglist[5])),
                    ('CodeChannel',int(msglist[6])),
                    ('AntennaDelayA',int(msglist[7])),
                    ('AntennaDelayB',int(msglist[8])),
                    ('ScanInfo',int(msglist[9])),
                    ('DisableCRERanges',bool(msglist[10])),
                    ('TransmitGain',int(msglist[11])),
                    ('ELR',bool(msglist[12][-2])),
                    ])
        return msg

    elif ' RcmP3XXConfig' == msglist[1] :
        #Timestamp, RcmP3XXConfig, NodeId, Channel, PRF, TxPreambleLength, TxRxPreambleCode, DataRate, NsSFD, RxLNA, SmartTxPwr, AntennaDelay, RangeInfo, ScanInfo, ELR,  OTA,  Persist
        #1444064949.001, RcmP3XXConfig, 107, 2,     64,  512,              9,                850,      True,  True,  False,      112,          0,         False,    True, False, False
        msg = dict([('msgType','RcmP3XXConfig'),
                    ('Timestamp',float(msglist[0])),
                    ('NodeID',msglist[2][1:]),
                    ('Channel',int(msglist[3])),
                    ('PRF',int(msglist[4])),
                    ('TxPreambleLength',int(msglist[5])),
                    ('TxRxPreambleCode',msglist[6][1:]),
                    ('DataRate',int(msglist[7])),
                    ('NsSFD',bool(msglist[8])),
                    ('RxLNA',bool(msglist[9])),
                    ('SmartTxPwr',bool(msglist[10])),
                    ('AntennaDelay',int(msglist[11])),
                    ('RangeInfo',int(msglist[12])),
                    ('ScanInfo',bool(msglist[13])),
                    ('ELR',bool(msglist[14])),
                    ('OTA',bool(msglist[15])),
                    ('Persist',bool(msglist[16]))
                    ])
        return msg

    elif ' RcmInternalDebugInfo' == msglist[1] :
        #Timestamp, RcmInternalDebugInfo, MessageId, MillisecondTimestamp, MicrosecondTimestamp, Message
        msg = dict([('msgType','RcmInternalDebugInfo'),
                    ('Timestamp',float(msglist[0])),
                    ('MessageId',int(msglist[2])),
                    ('MillisecondTimestamp',int(msglist[3])),
                    ('MicrosecondTimestamp',int(msglist[4])),
                    ])

        if ' KS2dM' == msglist[5] :
            #KS2dM, range, predictedRange, previousState[0], previousState[1], previousState[2],
            #previousState[3], anchorX, anchorY, anchorZ, timeDelta, m_localZHeight, reportedRangeErr,
            #sigmaAccel, state[0], state[1], state[2], state[3], covariance(0, 0), covariance(1, 1),
            #covariance(2, 2), covariance(3, 3), K[0], K[1], K[2], K[3]
            msg['dbgMsgType'] = 'KS2dM'
            therest = dict([('range',float(msglist[6])),
                    ('predictedRange',float(msglist[7])),
                    ('previousState',[float(msglist[8]),float(msglist[9]),float(msglist[10]), float(msglist[11])]),
                    ('anchorLoc',[ float(msglist[12]), float(msglist[13]), float(msglist[14]) ]),
                    ('timeDelta',float(msglist[15])),
                    ('m_localZHeight',float(msglist[16])),
                    ('reportedRangeErr',float(msglist[17])),
                    ('sigmaAccel',float(msglist[18])),
                    ('state',[float(msglist[19]),float(msglist[21]),float(msglist[22]),float(msglist[23])]),
                    ('covariance00',float(msglist[23])),
                    ('covariance11',float(msglist[24])),
                    ('covariance22',float(msglist[25])),
                    ('covariance33',float(msglist[26])),
                    ('K',[float(msglist[27]),float(msglist[28]),float(msglist[20]),float(msglist[30])]),
                    ])
            msg.update(therest)
        else :
            msg['dbgMsgType'] = 'MiscText'
            msg['Text'] = ''.join(msglist[5:])

        return msg

    elif ' RcmRangeInfo' == msglist[1] :
        #Timestamp, RcmRangeInfo, MessageId, ResponderId, RangeStatus, ReqAntennaMode, RespAntennaMode, StopwatchTime, PrecisionRangeMm, CoarseRangeMm, FilteredRangeMm, PrecisionRangeErrEstMm, CoarseRangeErrEstMm, FilteredRangeErrEstMm, FilteredRangeVelocityMmPerSec, FilteredRangeVelocityMmPerSecErrEst, RangeMeasurementType, ReqLEDFlags, RespLEDFlags, Noise, Vpeak, CoarseTOFInBins, EmbeddedTimestamp
        #1444409248.130, RcmRangeInfo, 1552, 114, 0, 1, 1, 23, 11819, 11819, 11819, 55, 55, 58, -1, 173, PCF, 8, 8, 248, 8690, 42473, 1154107
        msg = dict([('msgType','RcmRangeInfo'),
                    ('Timestamp',float(msglist[0])),
                    ('MessageID',int(msglist[2])),
                    ('ResponderID',int(msglist[3])),
                    ('RangeStatus',int(msglist[4])),
                    ('ReqAntennaMode',int(msglist[5])),
                    ('RespAntennaMode',int(msglist[6])),
                    ('StopwatchTime',int(msglist[7])),
                    ('PrecisionRange',float(msglist[8])/1000.0),
                    ('CoarseRangeMm',int(msglist[9])),
                    ('FilteredRangeMm',int(msglist[10])),
                    ('PrecisionRangeErrEst',float(msglist[11])/1000.0),
                    ('CoarseRangeErrEstMm',int(msglist[12])),
                    ('FilteredRangeErrEstMm',int(msglist[13])),
                    ('FilteredRangeVelocityMmPerSec',int(msglist[14])),
                    ('FilteredRangeVelocityMmPerSecErrEst',int(msglist[15])),
                    ('RangeMeasurementType',msglist[16][1:]),
                    ('ReqLEDFlags',int(msglist[17])),
                    ('RespLEDFlags',int(msglist[18])),
                    ('Noise',float(msglist[19])/1000.0),
                    ('Vpeak',float(msglist[20])/1000.0),
                    ('CoarseTOFInBins',int(msglist[21])),
                    ('EmbeddedTimestamp',float(msglist[21])/1000.0),
                    ])
        return msg

    elif ' RcmEchoedRangeInfo' == msglist[1] :
        #Timestamp, RcmEchoedRangeInfo, MessageId, RequesterId, ResponderId, PrecisionRangeMm, PrecisionRangeErrEstMm, LEDFlags, EmbeddedTimestamp
        #1443048424.559, RcmEchoedRangeInfo, 23686, 108,        117,         8475,             1345,                   6139,     895373747
        msg = dict([('msgType','RcmEchoedRangeInfo'),
                    ('Timestamp',float(msglist[0])),
                    ('MessageID',int(msglist[2])),
                    ('RequesterID',int(msglist[3])),
                    ('ResponderID',int(msglist[4])),
                    ('PrecisionRange',float(msglist[5])/1000.0),
                    ('PrecisionRangeErrEst',float(msglist[6])/1000.0),
                    ('LEDFlags',int(msglist[7])),
                    ('EmbeddedTimestamp',float(msglist[8])/1000.0),
                    ])
        return msg

    elif ' RcmScanInfo' == msglist[1] :
        #Timestamp, RcmScanInfo, MessageId, SourceId, AntennaId, LEDFlags, Noise, Vpeak, EmbeddedTimestamp, LeadingEdgeOffset, LockspotOffset, NumScanSamples, ScanData
        msg = dict([('msgType','RcmScanInfo'),
                    ('Timestamp',float(msglist[0])),
                    ('MessageID',int(msglist[2])),
                    ('SourceId',int(msglist[3])),
                    ('AntennaId',int(msglist[4])),
                    ('LEDFlags',int(msglist[5])),
                    ('Noise',int(msglist[6])),
                    ('Vpeak',int(msglist[7])),
                    ('EmbeddedTimestamp',int(msglist[8])),
                    ('LeadingEdgeOffset',int(msglist[9])),
                    ('LockspotOffset',int(msglist[10])),
                    ('NumScanSamples',int(msglist[11])),
                    ('ScanData',[int(i) for i in msglist[12:-1]]),
                    ])
        return msg

    elif ' RcmFullScanInfo' == msglist[1] :
        #Timestamp, RcmFullScanInfo, MessageId, SourceId, EmbeddedTimestamp, Noise, Vpeak, LeadingEdgeOffset, LockspotOffset, ScanStartPs, ScanStopPs, ScanStepBins, Filtering, AntennaId, Reserved, NumSamplesTotal, ScanData
        msg = dict([('msgType','RcmFullScanInfo'),
                    ('Timestamp',float(msglist[0])),
                    ('MessageID',int(msglist[2])),
                    ('SourceId',int(msglist[3])),
                    ('EmbeddedTimestamp',int(msglist[4])),
                    ('Noise',int(msglist[5])),
                    ('Vpeak',int(msglist[6])),
                    ('LeadingEdgeOffset',int(msglist[7])),
                    ('LockspotOffset',int(msglist[8])),
                    ('ScanStartPs',int(msglist[9])),
                    ('ScanStopPs',int(msglist[10])),
                    ('ScanStepBins',int(msglist[11])),
                    ('Filtering',int(msglist[12])),
                    ('AntennaId',int(msglist[13])),
                    ('LEDFlags',int(msglist[14])),
                    ('NumScanSamples',int(msglist[15])),
                    ('ScanData',[int(i) for i in msglist[16:-1]]),
                    ])
        return msg

    elif ' RcmSendRangeRequest' == msglist[1] :
        #Timestamp, RcmSendRangeRequest, MessageId, ResponderId, AntennaMode, DataSize, Data
        msg = dict([('msgType','RcmSendRangeRequest'),
                    ('Timestamp',float(msglist[0])),
                    ('MessageID',int(msglist[2])),
                    ('ResponderId',int(msglist[3])),
                    ('AntennaMode',int(msglist[4])),
                    ('DataSize',int(msglist[5])),
                    ('Data',[int(i) for i in msglist[6:-1]]),
                    ])
        return msg

    elif ' RnGetConfigConfirm' == msglist[1] :
        #Timestamp, RnGetConfigConfirm, MessageId, MaxNeighborAgeMs, AutosendUpdateIntervalMs, AutosendType, Flags, DefaultIf, DefaultIfAddr1, DefaultIfAddr2, EmbeddedTimestamp, Status
        #1444064949.002, RnGetConfigConfirm, 9, 10000, 300, 0, 0, 0, 0, 0, 5988158, 0
        msg = dict([('msgType','RnGetConfigConfirm'),
                    ('Timestamp',float(msglist[0])),
                    ('MessageID',int(msglist[2])),
                    ('MaxNeighborAgeMs',int(msglist[3])),
                    ('AutosendUpdateIntervalMs',int(msglist[4])),
                    ('AutosendType',int(msglist[5])),
                    ('Flags',int(msglist[6])),
                    ('DefaultIf',int(msglist[7])),
                    ('DefaultIfAddr1',int(msglist[8])),
                    ('DefaultIfAddr2',int(msglist[9])),
                    ('EmbeddedTimestamp',long(msglist[10])),
                    ('Status',int(msglist[11]))
                    ])
        return msg

    elif ' RnGetAlohaConfigConfirm' == msglist[1] :
        #Timestamp, RnGetAlohaConfigConfirm, MessageId, MinTimeBetweenTxMs, MaxTimeBetweenTxMs, MaxRequestDataSize, MaxResponseDataSize, Flags, Status
        #1444064949.003, RnGetAlohaConfigConfirm, 13, 10, 1990, 0, 0, 4, 0
        msg = dict([('msgType','RnGetAlohaConfigConfirm'),
                    ('Timestamp',float(msglist[0])),
                    ('MessageID',int(msglist[2])),
                    ('MinTimeBetweenTxMs',int(msglist[3])),
                    ('MaxTimeBetweenTxMs',int(msglist[4])),
                    ('MaxRequestDataSize',int(msglist[5])),
                    ('MaxResponseDataSize',int(msglist[6])),
                    ('Flags',int(msglist[7])),
                    ('Status',int(msglist[8]))
                    ])
        return msg

    elif ' RnFullNeighborDatabaseInfo' == msglist[1] :
        #Timestamp, RnFullNeighborDatabaseInfo, MessageId, NumNodes, SortType, EmbeddedTimestampMs, Status
        msg = dict([('msgType','RnFullNeighborDatabaseInfo'),
                    ('Timestamp',float(msglist[0])),
                    ('MessageID',int(msglist[2])),
                    ('NumNodes',int(msglist[3])),
                    ('SortType',int(msglist[4])),
                    ('EmbeddedTimestampMs',int(msglist[5])),
                    ('Status',int(msglist[6]))
                    ])
        return msg

    elif ' RnFullNeighborDatabaseEntry' == msglist[1] :
        #Timestamp, RnFullNeighborDatabaseEntry, NodeId, RangeStatus, AntennaMode, StopwatchTime,
        #RangeMm, RangeErrorEstimate, RangeVelocity, RangeMeasurementType, Flags, LedFlags, Noise,
        #Vpeak, StatsNumRangeAttempts, StatsNumRangeSuccesses, Stats
        msg = dict([('msgType','RnFullNeighborDatabaseEntry'),
                    ('Timestamp',float(msglist[0])),
                    ('NodeId',int(msglist[2])),
                    ('RangeStatus',int(msglist[3])),
                    ('AntennaMode',int(msglist[4])),
                    ('StopwatchTime',int(msglist[5])),
                    ('RangeMm',int(msglist[6])),
                    ('RangeErrorEstimate',int(msglist[7])),
                    ('RangeVelocity',int(msglist[8])),
                    ('RangeMeasurementType',int(msglist[9])),
                    ('Flags',int(msglist[10])),
                    ('LedFlags',int(msglist[11])),
                    ('Noise',int(msglist[12])),
                    ('Vpeak',int(msglist[13])),
                    ('StatsNumRangeAttempts',int(msglist[14])),
                    ('StatsNumRangeSuccesses',int(msglist[15])),
                    ('Stats',int(msglist[16]))
                    ])
        return msg

    elif ' NnConfig' == msglist[1] :
        #Timestamp, NnConfig, BootMode, LocationInfo,
        #RangeInfo, ReportELRs, ReportELLs, AutosendLDB, EnableNNRTP,
        #EnableSolverDBG, AutosendInterval, IncludeAnchor, IncludeMobile, SortLDB,
        #SolverMinREE, SolverMaxREE, RTPMaxLEE, Persist
        #11448050550.740, NnConfig, 11, 2, 2, 2, True, True, False, False, True, 0, False, False, 0, 0, 1000, 9999, True
        msg = dict([('msgType','NnConfig'),
                    ('Timestamp',float(msglist[0])),
                    ('BootMode',int(msglist[2])),
                    ('LocationInfo',bool(msglist[3])),

                    ('RangeInfo', bool(msglist[4])),
                    ('ReportELRs', bool(msglist[5])),
                    ('ReportELLs',bool(msglist[6])),
                    ('AutosendLDB',bool(msglist[7])),
                    ('EnableNNRTP',bool(msglist[8])),

                    ('EnableSolverDBG',bool(msglist[9])),
                    ('AutosendInterval',int(msglist[10])),
                    ('IncludeAnchor',bool(msglist[11])),
                    ('IncludeMobile',bool(msglist[12])),
                    ('SortLDB',bool(msglist[13])),

                    ('SolverMinREE',int(msglist[14])),
                    ('SolverMaxREE',int(msglist[15])),
                    ('RTPMaxLEE',int(msglist[16])),
                    ('Persist',bool(msglist[17]))
                    ])
        return msg

    # elif ' NnLocationMap' == msglist[1] :
    #     return []

    elif ' NnLocationMapEntry' == msglist[1] :
        # Timestamp, NnLocationMapEntry, NodeID, NodeType, XFixed,
        # YFixed, ZFixed, ZHemisphere, SendELRs, SendELLs,
        # ReportRangeInfos, BeaconIntervalMs, X, Y, Z
        # 1448050550.740, NnLocationMapEntry, 101, 2, False, False, False, 2, False, 1, 0, 0, 1116, 192, 2523
        nodeTypeI = int(msglist[3])
        nodeTypeList = ['Mobile','Anchor','Origin','+X','-X','+Y','-Y','Z']
        #pdb.set_trace()
        msg = dict([('msgType','NnLocationMapEntry'),
                    ('Timestamp',float(msglist[0])),
                    ('NodeID',int(msglist[2])),
                    ('NodeType',nodeTypeList[nodeTypeI]),#int(msglist[3])),
                    # ('XFixed',bool(msglist[4])),
                    # ('YFixed',bool(msglist[5])),
                    # ('ZFixed',bool(msglist[6])),
                    # ('ZHemisphere',int(msglist[7])),
                    ('SendELRs',bool(msglist[4])),
                    ('SendELLs',int(msglist[5])),
                    ('ReportRangeInfos',bool(msglist[6])),
                    ('BeaconIntervalMs',int(msglist[7])),
                    ('X',float(msglist[8])/1000.0),
                    ('Y',float(msglist[9])/1000.0),
                    ('Z',float(msglist[10])/1000.0)
                    ])
        return msg

    # elif ' NnWaypoints' == msglist[1] :
    #     return []

    elif ' NnWaypointEntry' == msglist[1] :
        #Timestamp, NnWaypointEntry, ID, X, Y, Z
        #1444064949.007, NnWaypointEntry, 1, 1038, 1286, 1233
        msg = dict([('msgType','NnWaypointEntry'),
                    ('Timestamp',float(msglist[0])),
                    ('ID',int(msglist[2])),
                    ('NodeType','Waypoint'),
                    ('X',float(msglist[3])/1000.0),
                    ('Y',float(msglist[4])/1000.0),
                    ('Z',float(msglist[5])/1000.0),
                    ])
        return msg

    # elif ' NnLocationInfo' == msglist[1] :
    #     #Timestamp, NnLocationInfo, MessageID, NodeID, NodeType, SolverStatus, XFixed, YFixed, ZFixed, ZHemisphere, X, Y, Z, XVariance, YVariance, ZVariance, XYCovariance, XZCovariance, YZCovariance, LocationErrorEstimate, LocationTimestampMs, MessageTimestamp
    #     msg = dict([('msgType','NnLocationInfo'),
    #                 ('Timestamp',float(msglist[0])),
    #                 ('MessageID',int(msglist[2])),
    #                 ('NodeID',int(msglist[3])),
    #                 ('NodeType',int(msglist[4])),
    #                 ('SolverStatus',int(msglist[5])),
    #                 ('XFixed',bool(msglist[6])),
    #                 ('YFixed',bool(msglist[7])),
    #                 ('ZFixed',bool(msglist[8])),
    #                 ('ZHemisphere',int(msglist[9])),
    #                 ('X',float(msglist[10])/1000.0),
    #                 ('Y',float(msglist[11])/1000.0),
    #                 ('Z',float(msglist[12])/1000.0),
    #                 ('XVariance',float(msglist[13])/1000.),
    #                 ('YVariance',float(msglist[14])/1000.),
    #                 ('ZVariance',float(msglist[15])/1000.),
    #                 ('XYCovariance',float(msglist[16])/1000.),
    #                 ('XZCovariance',float(msglist[17])/1000.),
    #                 ('YZCovariance',float(msglist[18])/1000.),
    #                 ('LocationErrorEstimate',float(msglist[19])/1000.),
    #                 ('LocationTimestampMs',long(msglist[20])),
    #                 ('MessageTimestamp',long(msglist[21])),
    #                 ])
    #     return msg

    elif ' NnEchoedLocationInfo' == msglist[1] :
        #Timestamp, NnEchoedLocationInfo, MessageId, NodeID, X, Y, Z, RemoteTimestamp
        #1444064949.218, NnEchoedLocationInfo, 2162, 118, 1091, 992, 1501, 647714
        msg = dict([('msgType','NnEchoedLocationInfo'),
                    ('Timestamp',float(msglist[0])),
                    ('MessageID',int(msglist[2])),
                    ('NodeID',int(msglist[3])),
                    ('X',float(msglist[4])/1000.),
                    ('Y',float(msglist[5])/1000.),
                    ('Z',float(msglist[6])/1000.),
                    ('RemoteTimestamp',long(msglist[7])),
                    ])
        return msg

    elif ' NnEchoLastLocationExInfo' == msglist[1] or ' NnLocationInfo' == msglist[1] :
        #Timestamp, NnLocationInfo, MessageID, NodeID, NodeType, SolverStage, SolverError, XFixed, YFixed, ZFixed, ZHemisphere, X, Y, Z, XVariance, YVariance, ZVariance, XYCovariance, XZCovariance, YZCovariance, DOP, NumAnchors, LocationTimestampMs, MessageTimestamp
        #pdb.set_trace()
        msg = dict([('msgType','NnEchoLastLocationExInfo'),
                    ('Timestamp',float(msglist[0])),
                    ('MessageID',int(msglist[2])),
                    ('NodeID',int(msglist[3])),
                    ('NodeType',int(msglist[4])),
                    ('SolverStage',int(msglist[5])),
                    ('SolverError',int(msglist[6])),
                    ('XFixed',bool(msglist[7])),
                    ('YFixed',bool(msglist[8])),
                    ('ZFixed',bool(msglist[9])),
                    ('ZHemisphere',int(msglist[10])),
                    ('X',float(msglist[11])/1000.0),
                    ('Y',float(msglist[12])/1000.0),
                    ('Z',float(msglist[13])/1000.0),
                    ('XVariance',float(msglist[14])/1000.),
                    ('YVariance',float(msglist[15])/1000.),
                    ('ZVariance',float(msglist[16])/1000.),
                    ('XYCovariance',float(msglist[17])/1000.),
                    ('XZCovariance',float(msglist[18])/1000.),
                    ('YZCovariance',float(msglist[19])/1000.),
                    #('LocationErrorEstimate',float(msglist[20])/1000.),
                    ('DOP',float(msglist[20])),
                    ('NumAnchors',int(msglist[21])),
                    ('LocationTimestampMs',long(msglist[22])),
                    ('MessageTimestamp',long(msglist[22])),
                    ])
        #pdb.set_trace()
        return msg

    elif ' LogfileMarker' == msglist[1] :
        msg = dict([('msgType','LogfileMarker'),
                    ('Timestamp',float(msglist[0])),
                    ('markerNum',int(msglist[2]))
                    ])
        return msg

    elif ' GameConfig' == msglist[1] :
        #Timestamp, GameConfig, WalkerInitials, CallerInitials, Waypoint1, Waypoint2, Waypoint3
        #1444409248.074, GameConfig, AA, BB, 2, 3, 1
        msg = dict([('msgType','GameConfig'),
                    ('Timestamp',float(msglist[0])),
                    ('WalkerInitials',msglist[2][1:]),
                    ('CallerInitials',msglist[3][1:]),
                    ('Waypoint1',int(msglist[4])),
                    ('Waypoint2',int(msglist[5])),
                    ('Waypoint3',int(msglist[6])),
                    ])
        return msg

    elif ' NnSetModeRequest' == msglist[1] :
        #Timestamp, NnSetModeRequest, MessageId, Mode, BroadcastFlag
        #1446502588.020, NnSetModeRequest, 19, 0, 1
        msg = dict([('msgType','NnSetModeRequest'),
                    ('Timestamp',float(msglist[0])),
                    ('MessageID',int(msglist[2])),
                    ('Mode',int(msglist[3])),
                    ('BroadcastFlag',int(msglist[4])),
                    ])
        return msg

    elif ' NnSetModeConfirm' == msglist[1] :
        #Timestamp, NnSetModeConfirm, MessageId, Mode, Status
        #1446502588.092, NnSetModeConfirm, 19, Idle, 0
        msg = dict([('msgType','NnSetModeConfirm'),
                    ('Timestamp',float(msglist[0])),
                    ('MessageID',int(msglist[2])),
                    ('Mode',msglist[3][1:]),
                    ('Status',int(msglist[4])),
                    ])
        return msg

    elif ' RangeNetUI' == msglist[1] :
        #Timestamp, RangeNetUI, Version
        #1449010345.865, RangeNetUI, 0.9.0.0
        msg = dict([('msgType','RangeNetUI'),
                    ('Timestamp',float(msglist[0])),
                    ('Version',msglist[2]),
                    ])

    elif ' AsConfig' == msglist[1] :
        #Timestamp, AsConfig, NodeCount, NodeID_Origin, NodeID_xAxis, NodeID_yAxis, xAxis_Sign, yAxis_Sign, PRME_Thresh, AlphaFilter
        #1446502607.486, AsConfig, 3, 101, 114, 109, 1, 1, 9999, 0.10
        msg = dict([('msgType','AsConfig'),
                    ('Timestamp',float(msglist[0])),
                    ('NodeCount',int(msglist[2])),
                    ('NodeID_Origin',int(msglist[3])),
                    ('NodeID_xAxis',int(msglist[4])),
                    ('NodeID_yAxis',int(msglist[5])),
                    ])

        if msg['NodeCount'] == 3 :
            msg['xAxis_Sign'] = int(msglist[6])
            msg['yAxis_Sign'] = int(msglist[7])
            msg['PRME_Thresh'] = float(msglist[8])/1000.0
            msg['AlphaFilter'] = float(msglist[9])
            msg['NodeIDs'] = map(int,msglist[3:6])

        if msg['NodeCount'] == 4 :
            msg['NodeID_zAxis'] = int(msglist[6])
            msg['xAxis_Sign'] = int(msglist[7])
            msg['yAxis_Sign'] = int(msglist[8])
            msg['PRME_Thresh'] = float(msglist[9])/1000.0
            msg['AlphaFilter'] = float(msglist[10])
            msg['NodeIDs'] = map(int,msglist[3:7])

        return msg

    elif ' AsRawNodes' == msglist[1] :
        #Timestamp, AsRawNodes, Ao_X, Ao_Y, Ao_Z, Ax_X, Ax_Y, Ax_Z, Ay_X, Ay_Y, Ay_Z
        #1446502607.486, AsRawNodes, 0.0000, 0.0000, 2.6020, 1.0000, 0.0020, 2.5970, 0.4490, 1.0000, 2.6050
        msg = dict([('msgType','AsRawNodes'),
                    ('Timestamp',float(msglist[0])),
                    ('Ao_X',float(msglist[2])),
                    ('Ao_Y',float(msglist[3])),
                    ('Ao_Z',float(msglist[4])),
                    ('Ax_X',float(msglist[5])),
                    ('Ax_Y',float(msglist[6])),
                    ('Ax_Z',float(msglist[7])),
                    ('Ay_X',float(msglist[8])),
                    ('Ay_Y',float(msglist[9])),
                    ('Ay_Z',float(msglist[10])),
                    ])
        msg['AsRawNodes'] = map(float,msglist[2:])

        return msg

    elif ' AsRangeList' == msglist[1] :
        #Timestamp, AsRangeList, AoAx_Range, AoAx_RangeErr, AoAy_Range, AoAy_RangeErr, AxAy_Range, AxAy_RangeErr
        #1446502608.935, AsRangeList, 12.6710, 0.0560, 6.6950, 0.1290, 12.4120, 0.0560
        msg = dict([('msgType','AsRangeList'),
                    ('Timestamp',float(msglist[0])),
                    ('AoAx_Range',float(msglist[2])),
                    ('AoAx_RangeErr',float(msglist[3])),
                    ('AoAy_Range',float(msglist[4])),
                    ('AoAy_RangeErr',float(msglist[5])),
                    ('AxAy_Range',float(msglist[6])),
                    ('AxAy_RangeErr',float(msglist[7])),
                    ])
        rangeList = map(float,msglist[2:])
        msg['AsRangeList'] = zip(*(iter(rangeList),) * 2)

        return msg

    elif ' AsFilteredNodes' == msglist[1] :
        #Timestamp, AsFilteredNodes, Ao_X, Ao_Y, Ao_Z, Ax_X, Ax_Y, Ax_Z, Ay_X, Ay_Y, Ay_Z
        #1443048434.929, AsFilteredNodes, 0, 0, 2557, 835, 449, 2554, 194, 601, 2549
        msg = dict([('msgType','AsFilteredNodes'),
                    ('Timestamp',float(msglist[0])),
                    ('Ao_X',float(msglist[2])),
                    ('Ao_Y',float(msglist[3])),
                    ('Ao_Z',float(msglist[4])),
                    ('Ax_X',float(msglist[5])),
                    ('Ax_Y',float(msglist[6])),
                    ('Ax_Z',float(msglist[7])),
                    ('Ay_X',float(msglist[8])),
                    ('Ay_Y',float(msglist[9])),
                    ('Ay_Z',float(msglist[10])),
                    ])
        msg['AsFilteredArray'] = map(float,msglist[2:])
        # rangeList = map(float,msglist[2:])
        # msg['AsRangeList'] = zip(*(iter(rangeList),) * 2)
        # asFiltArray = np.array(map(float,msglist[2:]))
        # print 'AsFilteredNodes: ', ['%.4f' % i for i in asFiltArray]
        # pyFiltArray = asv.locFilt.transpose().flatten()
        # print 'pyLocFilt: ', ['%.4f' % i for i in pyFiltArray]
        # diff = asFiltArray - pyFiltArray
        # print 'diff: ', ['%.4f' % i for i in diff]
        # locArray = np.reshape(asFiltArray,(asv.nodeCount,3)).transpose()
        return msg

    elif ' AsWeights' == msglist[1] :
        #Timestamp, AsWeights, AoAx_Weight, AoAy_Weight, AxAy_Weight
        #1443048434.929, AsWeights, 5.05, 2.53, 2.46
        msg = dict([('msgType','AsWeights'),
                    ('Timestamp',float(msglist[0])),
                    ('AoAx_Weight',float(msglist[2])),
                    ('AoAy_Weight',float(msglist[3])),
                    ('AxAy_Weight',float(msglist[4])),
                    ])
        msg['AsWeights'] = map(float,msglist[2:])
        return msg

    elif ' AsLocResidual' == msglist[1] :
        #Timestamp, AsLocResidual, LocResidual, LocResidualThreshold
        #1446502608.935, AsLocResidual, 16.7650, 0.300
        msg = dict([('msgType','AsLocResidual'),
                    ('Timestamp',float(msglist[0])),
                    ('LocResidual',float(msglist[2])),
                    ('LocResidualThreshold',float(msglist[3])),
                    ])
        return msg

    elif ' MrmConfig' == msglist[1] or ' Config' == msglist[1] :
        #Timestamp, MrmConfig, NodeId, ScanStartPs, ScanStopPs, ScanResolutionBins, BaseIntegrationIndex, Segment1NumSamples, Segment2NumSamples, Segment3NumSamples, Segment4NumSamples, Segment1AdditionalIntegration, Segment2AdditionalIntegration, Segment3AdditionalIntegration, Segment4AdditionalIntegration, AntennaMode, TransmitGain, CodeChannel
        msg = dict([('msgType','MrmConfig'),
                    ('Timestamp',float(msglist[0])),
                    ('NodeId',int(msglist[2])),
                    ('ScanStartPs',int(msglist[3])),
                    ('ScanStopPs',int(msglist[4])),
                    ('ScanResolutionBins',int(msglist[5])),
                    ('BaseIntegrationIndex',int(msglist[6])),
                    ('AntennaMode',int(msglist[15])),
                    ('TransmitGain',int(msglist[16])),
                    ('CodeChannel',int(msglist[17])),
                    ])
        return msg

    elif ' MrmControlRequest' == msglist[1]:
        #Timestamp, MrmControlRequest, ScanCount, IntervalTimeMicroseconds
        #1449345039.400, MrmControlRequest, 40, 65535, 100000,
        msg = dict([('msgType','MrmControlRequest'),
                    ('Timestamp',float(msglist[0])),
                    ('ScanCount',int(msglist[2])),
                    ('IntervalTimeMicroseconds',int(msglist[3])),
                    ])
        return msg

    elif ' MrmControlConfirm' == msglist[1] :
        #Timestamp, MrmControlConfirm, MessageId, Status
        #1449345039.416, MrmControlConfirm, 40, 0
        msg = dict([('msgType','MrmControlConfirm'),
                    ('Timestamp',float(msglist[0])),
                    ('MessageId',int(msglist[2])),
                    ('Status',int(msglist[3])),
                    ])
        return msg

    elif ' MrmFullScanInfo' == msglist[1]:
        #Timestamp, MrmFullScanInfo, MessageId, SourceId, EmbeddedTimestamp, Reserved, Reserved, Reserved, Reserved, ScanStartPs, ScanStopPs, ScanStepBins, Filtering, AntennaId, Reserved, NumSamplesTotal, ScanData
        msg = dict([('msgType','MrmFullScanInfo'),
                    ('Timestamp',float(msglist[0])),
                    ('MessageID',int(msglist[2])),
                    ('SourceId',int(msglist[3])),
                    ('EmbeddedTimestamp',long(msglist[4])),
                    ('ScanStartPs',int(msglist[9])),
                    ('ScanStopPs',int(msglist[10])),
                    ('ScanStepBins',int(msglist[11])),
                    ('Filtering',int(msglist[12])),
                    ('AntennaId',int(msglist[13])),
                    ('NumSamplesTotal',int(msglist[15])),
                    ('ScanData',[int(i) for i in msglist[16:-1]]),
                    ])
#        pdb.set_trace()
        return msg

    else :
        print '  parse SKIPPED: ', msglist[1]
