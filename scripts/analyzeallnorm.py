import scipy.stats
import scipy
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

LOC = {}
random = {}
swarm = {}
GA = {}
LOCswarm = {}
LOCGA = {}

def readdata(file,d):
    d["branch"] = []
    d["stmt"] = []
    d["fail"] = []
    for l in open(file):
        ls = l.split()
        d["branch"].append(float(ls[0]))
        d["stmt"].append(float(ls[1]))
        if ls[2] != "NA":
            d["fail"].append(float(ls[2]))

readdata("allnorm.LOC.alldata",LOC)
readdata("allnorm.random.alldata",random)            
readdata("allnorm.swarm.alldata",swarm)
readdata("allnorm.GA.alldata",GA)
readdata("allnorm.LOC+swarm.alldata",LOCswarm)
readdata("allnorm.LOC+GA.alldata",LOCGA)

def showField(field):
    print field+":"
    print "  LOC:",scipy.mean(LOC[field]),scipy.median(LOC[field]),scipy.std(LOC[field])
    print "  LOC+swarm:",scipy.mean(LOCswarm[field]),scipy.median(LOCswarm[field]),scipy.std(LOCswarm[field])
    print "  LOC+GA:",scipy.mean(LOCGA[field]),scipy.median(LOCGA[field]),scipy.std(LOCGA[field])
    print " ","-"*20
    print "  random:",scipy.mean(random[field]),scipy.median(random[field]),scipy.std(random[field])
    print "    ", scipy.stats.wilcoxon(LOC[field],random[field])
    print "  swarm:",scipy.mean(swarm[field]),scipy.median(swarm[field]),scipy.std(swarm[field])
    print "    ", scipy.stats.wilcoxon(LOCswarm[field],swarm[field])    
    print "  GA:",scipy.mean(GA[field]),scipy.median(GA[field]),scipy.std(GA[field])
    print "    ", scipy.stats.wilcoxon(LOCGA[field],GA[field])    


showField("branch")
showField("stmt")
showField("fail")

f1 = plt.figure(figsize=(5,2))

plt.ylabel("Branches covered")

def plotp(n):
    n = int(n * 100.0)
    if n < 0:
        return str(n)+"%"
    if n == 0:
        return str(n)+"%"
    return str(n)+"%"

plt.yticks((0,0.25,0.5,0.75,1.0),tuple(map(plotp,(0,0.25,0.5,0.75,1.0))))
plt.ylim(0,1.0)

plt.grid(axis='y')

plt.xlim(0.5,3.5)

plt.xticks(xrange(0,8),("","random","LOC","swarm","LOC\n+swarm","GA","LOC\n+GA"))


bb = plt.boxplot([random["branch"],LOC["branch"],swarm["branch"],LOCswarm["branch"],GA["branch"],LOCGA["branch"]],manage_xticks=False)

x1, y1 = [2.5, 2.5], plt.axis()[2:]
plt.plot(x1, y1,color='black')

x1, y1 = [4.5, 4.5], plt.axis()[2:]
plt.plot(x1, y1,color='black')


pp = PdfPages("normcovbranch.pdf")

pp.savefig(f1)
pp.close()
