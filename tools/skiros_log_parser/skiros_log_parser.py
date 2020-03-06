#!/usr/bin/env python

import re
import sys

_DUR = 1
_SUB_SKILL = 4
_STATE = 6
_MSG = 8
_SUB_SKILLS = [
    'ApplyPaintPrimitive',
    'ArmToZeroPrimitive',
    'LoadPaintPrimitive',
    'NavigateToLocationPrimitive',
    'task_plan']
_LOG_RE = re.compile('(.*;){8,8}.*')
_NAV_RE = re.compile('Reached \(.*, .*\) @ .* \[Delta: (.*), (.*)\]')

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

if len(sys.argv) < 2:
    print('File required')
    sys.exit(1)

with open(sys.argv[1]) as f:
    curr_data = ''
    tracking = False

    line = f.readline()
    while line:
        data, line = read_entry(line, f)

        # New skill started
        if tracking and data[_SUB_SKILL] != curr_data[_SUB_SKILL]:
            if curr_data[_SUB_SKILL] == 'NavigateToLocationPrimitive':
                m = _NAV_RE.match(curr_data[_MSG])
                print('{},{},{},{}'.format(curr_data[_SUB_SKILL], float(curr_data[_DUR]), m.group(1), m.group(2)))
            else:
                print('{},{}'.format(curr_data[_SUB_SKILL], float(curr_data[_DUR])))

        if data[_SUB_SKILL] in _SUB_SKILLS and data[_STATE] in ('Running', 'Success'):
            curr_data = data
            tracking = True
        else:
            curr_data = None
            tracking = False
