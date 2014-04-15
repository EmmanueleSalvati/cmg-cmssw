#! /usr/bin/env python
from optparse import OptionParser

import os.path
import sys, re

if __name__ == '__main__':

    odir = "/store/cmst3/user/lucieg/CMG/"+sys.argv[1]+"/SUSY"

    for i in range(0, 25) :
        os.system("mkdir -p ./%s/"%(sys.argv[1]))
        os.system("cp susy_cfg.py ./%s/susy_cfg_%s.py"%(sys.argv[1],str(i)))
        os.system("sed 's|ITER|%s|' ./%s/susy_cfg_%s.py > ./%s/susy_cfg_%s_tmp.py"%(str(i),sys.argv[1],str(i),sys.argv[1],str(i)))
        os.system("sed 's|DATASET|%s|' ./%s/susy_cfg_%s_tmp.py > ./%s/susy_cfg_%s.py"%(sys.argv[1],sys.argv[1],str(i),sys.argv[1],str(i)))
        os.system("rm ./%s/susy_cfg_%s_tmp.py"%(sys.argv[1],str(i)))
        logs = "/afs/cern.ch/work/l/lucieg/private/"+sys.argv[1]+"_"+str(i)
        #print logs
        #os.system("echo 'cmsBatch.py 100 tmp/susy_cfg_%s.py  -r %s -b 'bsub -q 8nh < ./batchScript.sh' -f -o tmp%s -n'"%(odir,str(i),logs))
        os.system("cmsBatch.py 1 %s/susy_cfg_%s.py  -r %s -b 'bsub -q 8nh < ./batchScript.sh' -f -o %s --notagCVS"%(sys.argv[1],str(i),odir,logs))
