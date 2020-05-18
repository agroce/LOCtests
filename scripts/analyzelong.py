import scipy
import scipy.stats
import glob
import os
import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

LOCdata = []
randomdata = []
for f in glob.glob("run1hour.sampleprobs.out.*"):
    currLOCdata = []
    hadFinal = False
    for l in open(f):
        if "branches" in l:
            branches = int(l.split("branches")[0].split()[-1])
            currLOCdata.append(branches)
        if "BRANCHES COVERED" in l:
            currLOCdata.append(int(l.split()[0]))
            hasFinal = True            
    if hasFinal:
        LOCdata.append(currLOCdata)

for f in glob.glob("run1hour.random.out.*"):
    currrandomdata = []
    hadFinal = False
    for l in open(f):
        if "branches" in l:
            branches = int(l.split("branches")[0].split()[-1])
            currrandomdata.append(branches)
        if "BRANCHES COVERED" in l:
            currrandomdata.append(int(l.split()[0]))           
            hasFinal = True
    if hasFinal:
        randomdata.append(currrandomdata)

LOCmeans = []
LOCerrors = []
randommeans = []
randomerrors = []
        
for i in xrange(max(map(len,LOCdata))):
    print "TIMESTAMP",i,
    LOCtime = []
    randomtime = []
    for d in LOCdata:
        try:
            LOCtime.append(d[i])
        except:
            pass
    for d in randomdata:
        try:
            randomtime.append(d[i])
        except:
            pass

    LOCmeans.append(scipy.mean(LOCtime))
    randommeans.append(scipy.mean(randomtime))    
    print scipy.mean(LOCtime),scipy.mean(randomtime)
    LOCconf = scipy.stats.norm.interval(0.95,loc=scipy.mean(LOCtime),scale=scipy.std(LOCtime)/math.sqrt(len(LOCtime)))
    randomconf = scipy.stats.norm.interval(0.95,loc=scipy.mean(randomtime),scale=scipy.std(randomtime)/math.sqrt(len(randomtime)))
    print LOCconf,LOCconf[1]-scipy.mean(LOCtime)
    print randomconf,randomconf[1]-scipy.mean(randomtime)
    if not scipy.isnan(LOCconf[1]):
        LOCerrors.append(LOCconf[1] - scipy.mean(LOCtime))
    else:
        LOCerrors.append(0)
    if not scipy.isnan(randomconf[1]):
        randomerrors.append(randomconf[1] - scipy.mean(randomtime))
    else:
        randomerrors.append(0)


f1 = plt.figure(figsize=(8,2))

plt.ylabel("Branches covered")
plt.xlabel("Minutes")

plt.grid(axis='y')

#plt.plot(LOCmeans)
#plt.plot(randommeans)

for i in xrange(0,120):
    plt.errorbar([(i+0.30)/2.0],[LOCmeans[i]], yerr=LOCerrors[i],color='green')
    plt.errorbar([(i+0.30)/2.0],[randommeans[i]], yerr=randomerrors[i],color='red')
    
m = min(randommeans+LOCmeans)-randomerrors[0]
v = max(LOCmeans+randommeans)-min(randommeans)


plt.plot([52],[m+(v*0.02)],'ro')
plt.plot([52],[m+(v*0.17)],'go')
plt.text(53,m,"random",color="red")
plt.text(53,m+(v*0.15),"LOC",color="green")
    
f1.show()
    
pp = PdfPages("longruns.pdf")
pp.savefig(f1)
pp.close()
    
