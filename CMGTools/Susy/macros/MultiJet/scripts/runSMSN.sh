#!/bin/bash

mlsp=$1

export DIR=/afs/cern.ch/user/l/lucieg/scratch1/Ap18/CMGTools/CMSSW_5_3_9/src/CMGTools/Susy/
echo "python $DIR/macros/MultiJet/razorMJDataset.py datasetName="$SMS" maxFiles=10 index=$2 outputDirectory=/data/lucieg/RazorMultiJet/mLSP${mlsp}/ mLSP=${mlsp}"
python $DIR/macros/MultiJet/razorMJDataset.py datasetName="$SMS" maxFiles=10 index=$2 mLSP=${mlsp} outputDirectory=/data/lucieg/RazorMultiJet/mLSP${mlsp}
