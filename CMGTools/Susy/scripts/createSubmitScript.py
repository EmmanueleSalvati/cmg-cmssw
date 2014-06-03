#!/usr/bin/env python
"""Takes two numbers: first, and last job as input and the log directory.
It returns a submitJobs.sh file to submit jobs for skimming susy trees"""

import sys

if __name__ == '__main__':

    ARGS = sys.argv[1:]
    if not ARGS:
        print 'usage: first_job last_job log_directory'
        sys.exit(1)


    FIRST_JOB = int(sys.argv[1])
    LAST_JOB = int(sys.argv[2])
    LOG_DIR = sys.argv[3]
    SUBMIT_FILE = open("submitJobs.sh", "w")
    SUBMIT_FILE.write("#$ -S /bin/sh\n\n")

    for i in range(FIRST_JOB, LAST_JOB+1):
    # for i in [10, 20, 41, 42, 51, 64, 67, 70]:
        SUBMIT_FILE.write("cd %s/Job_%s\n" %(LOG_DIR, str(i)))
        SUBMIT_FILE.write("echo \"Submitting job %s\"\n" %str(i))
        SUBMIT_FILE.write("ls\n")
        SUBMIT_FILE.write("qsub ./batchScript.sh\n")
        SUBMIT_FILE.write("cd -\n")

    SUBMIT_FILE.close()
