#!/bin/bash

mlsp=$1

seq 0 200 | xargs --max-procs=12 -n 1 bash ./runSMSN.sh ${mlsp}
#seq 0 300 | xargs --max-procs=12 -n 1 bash ./runSMSN.sh 