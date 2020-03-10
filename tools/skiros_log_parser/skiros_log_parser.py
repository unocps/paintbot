#!/usr/bin/env python

import re
import sys

_DUR = 1
_SUB_SKILL = 4
_STATE = 6
_CODE = 7
_MSG = 8
_SUB_SKILLS = [
    'ApplyPaintPrimitive',
    'ArmToZeroPrimitive',
    'LoadPaintPrimitive',
    'NavigateToLocationPrimitive',
    'task_plan']
_LOG_RE = re.compile('(.*;){8,8}.*')
_NAV_RE = re.compile('Reached \(.*, .*\) @ .* \[Delta: (.*), (.*), Dist: (.*)\]')

def read_entry(line, f):
    data = line.split(';')
    if _LOG_RE.match(line):
        line = f.readline()
        if not line:
            return data, line
        while not _LOG_RE.match(line):
            data[_MSG] += line
            line = f.readline()
    return data, line

def print_stats(stats):
    print(','.join('{}' for i in range(len(stats))).format(*stats))

if len(sys.argv) < 2:
    print('File required')
    sys.exit(1)

with open(sys.argv[1]) as f:
    track_data = None

    line = f.readline()
    while line:
        data, line = read_entry(line, f)

        if data[_STATE] == 'Failure':
            print_stats((data[_SUB_SKILL], int(data[_CODE]), float(data[_DUR])))
        elif track_data and data[_SUB_SKILL] != track_data[_SUB_SKILL]:
            if track_data[_SUB_SKILL] == 'NavigateToLocationPrimitive':
                print('NavigateToLocationPrimitive')
                m = _NAV_RE.match(track_data[_MSG])
                print_stats((track_data[_SUB_SKILL], int(track_data[_CODE]), float(track_data[_DUR]), m.group(1), m.group(2), m.group(3)))
            else:
                print('else')
                print_stats((track_data[_SUB_SKILL], int(track_data[_CODE]), float(track_data[_DUR])))

        if data[_SUB_SKILL] in _SUB_SKILLS and data[_STATE] in ('Running', 'Success'):
            track_data = data
        else:
            track_data = None
