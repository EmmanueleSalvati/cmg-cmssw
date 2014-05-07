#!/usr/bin/env python

import sys

if __name__ == '__main__':

    args = sys.argv[1:]
    if not args:
        print 'usage: first_job last_job log_directory'
        sys.exit(1)


    firstJob = int(sys.argv[1])
    lastJob = int(sys.argv[2])
    logDir = sys.argv[3]
    submitFile = open("submitJobs.sh", "w")
    submitFile.write("#$ -S /bin/sh\n\n")

    for i in range(firstJob, lastJob+1):
        submitFile.write("cd %s/Job_%s\n" %(logDir, str(i)))
        submitFile.write("echo \"Submitting job %s\"\n" %str(i))
        submitFile.write("ls\n")
        submitFile.write("qsub ./batchScript.sh\n")
        submitFile.write("cd -\n")

    submitFile.close()
