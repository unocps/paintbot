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
    curr_skill = ''
    duration = ''
    tracking = False

    line = f.readline()
    while line:
        data, line = read_entry(line, f)

        # New skill started
        if tracking and data[_SUB_SKILL] != curr_skill:
            print('{},{}'.format(curr_skill, float(duration)))

        if data[_SUB_SKILL] in _SUB_SKILLS and data[_STATE] in ('Running', 'Success'):
            curr_skill = data[_SUB_SKILL]
            duration = data[_DUR]
            tracking = True
        else:
            curr_skill = ''
            duration = ''
            tracking = False
