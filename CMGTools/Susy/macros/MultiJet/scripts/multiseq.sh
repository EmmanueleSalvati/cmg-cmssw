#!/bin/bash

mlsp=$1

mkdir -p /data/lucieg/RazorMultiJet/mLSP${mlsp}

for exp in $(cat exportSMS);
do
export $exp
echo $SMS
bash seq.sh $mlsp
done;
