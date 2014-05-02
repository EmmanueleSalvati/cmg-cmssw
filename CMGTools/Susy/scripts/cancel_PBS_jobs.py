#!/usr/bin/env python
"""Script to remove a range of jobs from the PBS queues"""

import sys
import os

if __name__ == '__main__':
    ARGS = sys.argv[1:]
    if not ARGS:
        print 'usage: cancel_PBS_jobs.py <first-number> <last-number>'
        sys.exit(1)

    FIRST_NUMBER = int(ARGS[0])
    LAST_NUMBER = int(ARGS[1])

    for i in range(FIRST_NUMBER, LAST_NUMBER+1):
        CMD = 'qdel ' + str(i) + '.nys1.cac.cornell.edu'
        print CMD
        os.system(CMD)
