import subprocess

TIMEOUT = "60"

for i in xrange(0,100):
    print "EXPERIMENT",i
    rname = "nonguided." + TIMEOUT + "." + str(i) + ".out"
    gname = "dguided." + TIMEOUT + "." + str(i) + ".out"
    gfname = "sampguided." + TIMEOUT + "." + str(i) + ".out"
    statname = "statguided." + TIMEOUT + "." + str(i) + ".out"
    oldname = "oldsampguided." + TIMEOUT + "." + str(i) + ".out"
    sname = "sguided." + TIMEOUT + "." + str(i) + ".out"
    pswarmname = "probswarmguided." + TIMEOUT + "." + str(i) + ".out"
    pganame = "exploitguided." + TIMEOUT + "." + str(i) + ".out"
    mname = "exploit08." + TIMEOUT + "." + str(i) + ".out"
    mname2 = "exploit02." + TIMEOUT + "." + str(i) + ".out"    
    r = 152
    while r == 152:
        r = subprocess.call(["ulimit -t 400; tstl_rt --full --silentFail  --multiple --probs locsample.probs --timeout " + TIMEOUT + " >& " + gfname], shell=True)    
    r = 152
    while r == 152:
        r = subprocess.call(["ulimit -t 400; tstl_rt --full --silentFail  --multiple --LOCProbs --timeout " + TIMEOUT + " >& " + statname], shell=True)    
    r = 152
    while r == 152:
        r = subprocess.call(["ulimit -t 400; tstl_rt --full --silentFail  --multiple --timeout " + TIMEOUT + " >& " + rname], shell=True)
    r = 152
    while r == 152:
        r = subprocess.call(["ulimit -t 400; tstl_rt --full --silentFail  --multiple --swarm --timeout " + TIMEOUT + " >& " + sname], shell=True)
    r = 152
    while r == 152:
        r = subprocess.call(["ulimit -t 400; tstl_rt --full --silentFail --multiple --exploit 0.8 --Pmutate 0.8 --timeout " + TIMEOUT + " >& " + mname], shell=True)
    r = 152
    while r == 152:
        r = subprocess.call(["ulimit -t 400; tstl_rt --full --silentFail  --multiple --swarm --probs locsample.probs --timeout " + TIMEOUT + " >& " + pswarmname], shell=True)
    r = 152
    while r == 152:
        r = subprocess.call(["ulimit -t 400; tstl_rt --full --silentFail --multiple --probs locsample.probs --exploit 0.8 --Pmutate 0.8 --timeout " + TIMEOUT + " >& " + pganame], shell=True)    
