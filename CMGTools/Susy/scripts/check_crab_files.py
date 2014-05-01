#!/usr/bin/env python

"""This module checks if there are missing files, simply by looking
at the file numbers. It requires a txt file with the list of
cmgTuple_XX_yyy.root, without the full path"""

import sys

if __name__ == '__main__':
    ARGS = sys.argv[1:]

    if not ARGS:
        print "Usage: ./check_crab_files.py [--file-number <number>]\
            <crabjobs.txt>"
        sys.exit(1)

    TEXT_FILE = open(ARGS[-1])

    TOTAL_LIST = []
    LINE_COUNT = 0
    for line in TEXT_FILE:
        firstString = line.split('_')
        fileNumber = int(firstString[-3])
        TOTAL_LIST.append(fileNumber)

    TOTAL_LIST.sort()

    print "I have this number of files:", len(TOTAL_LIST)

    MISSING_LIST = []

    if len(ARGS) > 1:
        LAST_ELEMENT = int(ARGS[1])
    else:
        LAST_ELEMENT = TOTAL_LIST[len(TOTAL_LIST)-1]

    for i in range(1, LAST_ELEMENT):
        if not i in TOTAL_LIST:
            LINE_COUNT += 1
            MISSING_LIST.append(str(i))

    print "Number of missing lines", LINE_COUNT
    MISSING_NUMBERS = ",".join(MISSING_LIST)
    print MISSING_NUMBERS
