import os, sys

if __name__ == '__main__':

    mLSP   = sys.argv[1]

    for mStop in range(150, 825, 25):
        for box in ['Ele','Mu','BJetHS','BJetLS']:
            os.system("python plotDistributions.py %s %s %s.0"%(box, mLSP, mStop))
