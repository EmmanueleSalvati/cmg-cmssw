#! /usr/bin/env python
"""This script is to submit a set of PBS jobs to create the final TTrees,
susy_tree.root files"""

import os
import sys

if __name__ == '__main__':
    ARGS = sys.argv[1:]
    if not ARGS:
        print 'Usage: run_Razor_MJ_dataset.py <number_of_jobs>'
        sys.exit(1)

    DATA_SET = "Run2012D-part1_10Dec2012-v1"
    DATA_SET_DIR = "Run2012D-part1_10Dec2012-v1_3/"
    SUBMIT_DIR = "submit_" + DATA_SET
    print SUBMIT_DIR
    INPUT_DIR = 'root://osg-se.cac.cornell.edu//xrootd/path/cms/'\
        'store/user/salvati/Razor/MultiJet2012/CMSSW_5_3_14/'\
        'CMGTuples_skimmed/' + DATA_SET_DIR
    OUT_DIR = '/store/user/salvati/Razor/MultiJet2012/'\
        'CMSSW_5_3_14/SusyTrees/%s' % DATA_SET_DIR

    LOG_DIR = "step3_Run2012D-part1_10Dec2012-v1_3/"

    os.system("mkdir %s" % SUBMIT_DIR)
    os.system("mkdir %s" % LOG_DIR)

    # N_FILES = int(sys.argv[1])
    N_FILES = int(ARGS[0])

    PWD = os.environ['PWD']

    for i in range(1, N_FILES+1):
        fileName = 'susy_tree_%s.root' % str(i)
        runScriptName = SUBMIT_DIR + "/batchscript_%s_%s.sh"\
            % (DATA_SET, str(i))
        runScript = open(runScriptName, 'w')
        runScript.write('#$ -S /bin/sh\n')
        runScript.write('#$ -l arch=lx24-amd64\n')
        runScript.write('#PBS -m ea\n')
        runScript.write('#PBS -M es575@cornell.edu\n')
        runScript.write('#$ -l mem_total=2G\n')
        runScript.write('#PBS -j oe\n\n')
        runScript.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n\n')
        runScript.write('export SCRAM_ARCH=slc5_amd64_gcc462\n')
        runScript.write('cd %s\n' % PWD)
        runScript.write('eval `scramv1 runtime -sh`\n')
        runScript.write('python macros/MultiJet/razorMJDataset.py '
            'outputFile=/tmp/%s runOnMC=False datasetName=%s '\
            'inputFiles=%s%s\n\n' % (fileName, INPUT_DIR, INPUT_DIR, fileName))
        runScript.write('xrdcp /tmp/%s root://osg-se.cac.cornell.edu/'\
            '/xrootd/path/cms/%s%s\n' % (fileName, OUT_DIR, fileName))
        runScript.write('rm -f /tmp/%s\n\n' % fileName)
        runScript.write('exit')

        runScript.close()
        os.system('echo qsub %s -o %s' % (runScriptName, LOG_DIR))
        # os.system('qsub %s -o %s' % (runScriptName, LOG_DIR))
