import os
import sys

if __name__ == '__main__':
    dataSet = "Run2012D-part1_10Dec2012-v1"
    dataSetDirectory = "Run2012D-part1_10Dec2012-v1_3/"
    submitDir = "submit_" + dataSet
    inputDir = "root://osg-se.cac.cornell.edu//xrootd/path/cms/store/user/salvati/Razor/MultiJet2012/CMSSW_5_3_14/CMGTuples_skimmed/" + dataSetDirectory
    physicalInputDir = inputDir.replace('/store/','/mnt/xrootd/')
    outDir = "/store/user/salvati/Razor/MultiJet2012/SusyTrees/MultiJet1Parked/%s" % dataSetDirectory

    logDir = "step3_Run2012D-part1_10Dec2012-v1_3/"

    os.system("mkdir %s" % submitDir)
    os.system("mkdir %s" % logDir)

    # Find the number of files in the input directory
    # nFiles = len(os.listdir(physicalInputDir))
    nFiles = int(sys.argv[1])

    pwd = os.environ['PWD']

    for i in range(1, nFiles+1):
        if i == 7 or i == 8:
            continue
        fileName = 'susy_tree_%s.root' % str(i)
        runScriptName = submitDir + "/batchscript_%s_%s.sh" % (dataSet, str(i))
        runScript = open(runScriptName, 'w')
        runScript.write('#$ -S /bin/sh\n')
        runScript.write('#$ -l arch=lx24-amd64\n')
        runScript.write('#PBS -m ea\n')
        runScript.write('#PBS -M es575@cornell.edu\n')
        runScript.write('#$ -l mem_total=2G\n')
        runScript.write('#PBS -j oe\n\n')
        # runScript.write('export SCRAM_ARCH=slc5_amd64_gcc434\n')
        runScript.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n\n')
        runScript.write('cd %s\n' % pwd)
        runScript.write('eval `scramv1 runtime -sh`\n')
        runScript.write('python macros/MultiJet/razorMJDataset.py outputFile=/tmp/%s runOnMC=False datasetName=%s inputFiles=%s/%s\n\n' % (fileName, inputDir, inputDir, fileName))
        runScript.write('xrdcp /tmp/%s root://osg-se.cac.cornell.edu//xrootd/path/cms/%s%s\n' % (fileName, outDir, fileName))
        runScript.write('rm -f /tmp/%s\n\n' % fileName)
        runScript.write('exit')

        runScript.close()
        os.system('echo qsub %s -o %s' % (runScriptName, logDir))
        os.system('qsub %s -o %s' % (runScriptName, logDir))
