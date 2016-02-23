#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
pickel_log(ffn_in)
creates pickle binary form of RangeNet .csv logfile to pickle binary form
"""

import pdb
import os, sys
import numpy as np
import pprint as pp
from query_file import query_file
from parse_msg import parse_msg
import pickle

ffn_in = []
if not ffn_in :  # if empty
    ffn_in = query_file()

with open(ffn_in,'r') as f:
    iline = 0

    log_list = []
    for line in f:
        iline += 1
        print '%d: %s' % (iline,line[0:99].strip('\n'))

        msg = parse_msg(line)

        # Get rid of short or blank lines
        if not msg or len(line) < 5:
            continue

        log_list.append(msg)

# Create pkl file
path,fn_in = os.path.split(ffn_in)
fn_main,fn_ext = os.path.splitext(fn_in)
fn_pkl = fn_main + '.pkl'
ffn_pkl = os.path.join(path,fn_pkl)

fh_pkl = open(ffn_pkl,'wb')
pickle.dump(log_list,fh_pkl)
fh_pkl.close()
print 'Compressed data saved to ', ffn_pkl
