# -*- coding: utf-8 -*_
"""
# created: Mi 17. Jun 16:37:07 CEST 2020
# description: timekeeper-tool with checkin/checkout
# author: Mauritz Mälzer
# github: d2dugas
"""

import sys
import pandas as pd
from datetime import datetime
from argparse import ArgumentParser

parser = ArgumentParser(description='timekeeper tool')
parser.add_argument('--cmd', required=True,
            help='timekeeper command to be executed (checkin, checkout, etc.)')
parser.add_argument('--frame', help='first and last index to be summed over',
                    nargs='+', type=int, required=False)
args = parser.parse_args()
print(args)

if args.cmd == 'init':
    df = pd.DataFrame(columns=['timestamp', 'action'])
    df.to_pickle('df.pickle')

df = pd.read_pickle('df.pickle')

if args.cmd == 'checkin':
    df = df.append({'timestamp': datetime.now(), 'action': 'in'},
                   ignore_index=True)
elif args.cmd == 'checkout':
    df = df.append({'timestamp': datetime.now(), 'action': 'out'},
                   ignore_index=True)
elif args.cmd == 'print':
    print(df)
elif args.cmd == 'sum':
    start = args.frame[0]
    finish = args.frame[1]
    t1 = 0
    t2 = 0
    sum_seconds = 0
    # sum entries specified in args
    for index, row in df.iloc[start:(finish + 1)].iterrows():
        if row.action == 'in':
            t1 = row.timestamp
        elif row.action == 'out':
            t2 = row.timestamp
            duration = t2 - t1
            sum_seconds += duration.total_seconds()
    # add till now if last entry == 'in'
    if df.iloc[-1].action == 'in':
        sum_seconds += (datetime.now() - df.iloc[-1].timestamp).total_seconds()
    hours = divmod(sum_seconds, 3600)
    minutes = divmod(hours[1], 60)
    print('Checkin time: {0} hours, {1} minutes'.format(
          hours[0], minutes[0]))

df.to_pickle('df.pickle')
