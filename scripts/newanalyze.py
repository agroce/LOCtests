import scipy
import scipy.stats
import glob
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

data = {}

TIMEOUT = "60"

category = {"sampguided":"LOC",
            "statguided":"LOC(stat)",
            "oldsampguided":"LOC(old)",
            "probswarmguided":"LOC+swarm",
            "exploitguided":"LOC+GA",
            "nonguided":"random",
            "sguided":"swarm",
            "exploit08":"GA"}
                
anyFailed = False

baselineB = None
baselineS = None
if os.path.exists("baseline.out"):
    for l in open("baseline.out"):
        if "BRANCH" in l:
            baselineB = int(l.split()[2])
        if "STATEMENT" in l:
            baselineS = int(l.split()[2])            
        

for v in category.values():
    data[v] = {}
    data[v]["branch"] = []
    data[v]["stmt"] = []
    data[v]["fail"] = []
    data[v]["branch30"] = []
    data[v]["stmt30"] = []
    data[v]["fail30"] = []        

bmax = 0
    
for f in glob.glob("*guided." + TIMEOUT + ".*.out")+glob.glob("exploit0*." + TIMEOUT + ".*.out"):
    fname = f.split(".")[0]
    if fname not in category:
        continue    
    hit30 = False
    b = None
    fc = 0
    fc30 = 0
    for l in open(f):
        if "BRANCHES COVERED" in l:
            b = int(l.split()[0])
        if "STATEMENTS COVERED" in l:
            s = int(l.split()[0])
        if "LOGGED REPLAY" in l:
            anyFailed = True
            if not hit30:
                fc30 += 1
        if "stmts" in l:
            hit30 = True
            b30 = int(l.split()[13])
            s30 = int(l.split()[11])
        if "FAILED" in l:
            fc = int(l.split()[0])
    if b == None:
        print "NO BRANCH DATA FOR FILE",f
        continue
    tdata = category[fname]

    if b > bmax:
        bmax = b
    
    data[tdata]["branch"].append(b)
    data[tdata]["stmt"].append(s)
    data[tdata]["branch30"].append(b30)
    data[tdata]["stmt30"].append(s30)
    data[tdata]["fail"].append(fc)
    data[tdata]["fail30"].append(fc30)    

for cat in data:
    print cat,len(data[cat]["branch"])
    
for field in ["branch30","stmt30","fail30","branch","stmt","fail"]:
    if "fail" in field and not anyFailed:
        continue
    print "="*60
    print field.upper()+":"
    for cat in ["LOC","LOC(stat)","LOC(old)","random","swarm","GA","LOC+swarm","LOC+GA"]:
        if len(data[cat][field]) == 0:
            continue
        print "  "+cat+":",scipy.mean(data[cat][field]),scipy.std(data[cat][field])
        if cat != "LOC":
            try:
                sr = scipy.stats.mannwhitneyu(data[cat][field],data["LOC"][field])
                print "    vs. LOC:",sr
            except ValueError:
                pass
        if cat != "GA":
            try:
                sr = scipy.stats.mannwhitneyu(data[cat][field],data["GA"][field])
                print "    vs. GA:",sr
            except ValueError:
                pass
        if cat != "swarm":
            try:
                sr = scipy.stats.mannwhitneyu(data[cat][field],data["swarm"][field])
                print "    vs. swarm:",sr
            except ValueError:
                pass                        
        if (cat != "LOC") and (cat != "random"):
            try:
                sr = scipy.stats.mannwhitneyu(data[cat][field],data["random"][field])
                print "    vs. random:",sr
            except ValueError:
                pass
    locField = scipy.mean(data["LOC"][field])
    randomField = scipy.mean(data["random"][field])    
    print "GAIN OR LOSS VS. RANDOM:",str(((locField-randomField)/randomField)*100.0)+"%"

print "="*80

tlist = []
for f in glob.glob("howlong.*.*.out"):
    for l in open(f):
        if "DUE TO REACHING BRANCH COVERAGE TARGET, TERMINATED AT LENGTH" in l:
            tlist.append(float(l.split()[-1]))
            break
        if "TOTAL RUNTIME" in l:
            tlist.append(float(l.split()[0]))
            break

if tlist != []:
    print "AVERAGE TIME TO REACH SAME BRANCH COV:",scipy.mean(tlist),scipy.std(tlist)
    print "= ",scipy.mean(tlist)/60.0,"more test time"

tlist = []
for f in glob.glob("howlong2.*.*.out"):
    for l in open(f):
        if "DUE TO REACHING BRANCH COVERAGE TARGET, TERMINATED AT LENGTH" in l:
            tlist.append(float(l.split()[-1]))
            break
        if "TOTAL RUNTIME" in l:
            tlist.append(float(l.split()[0]))
            break

if tlist != []:
    print "AVERAGE TIME TO REACH SAME BRANCH COV (OTHER DIRECTION):",scipy.mean(tlist),scipy.std(tlist)
    print "= ",scipy.mean(tlist)/60.0,"more test time"


if baselineB != None:
    print "*"*80
    for field in ["branch30","stmt30","branch","stmt"]:
        if "branch" in field:
            baseline = baselineB
        else:
            baseline = baselineS
        randVal = scipy.mean(data["random"][field]) - baseline
        LOCVal = scipy.mean(data["LOC"][field]) - baseline
        print field,"ADJUSTED GAIN/LOSS OVER RANDOM:",((LOCVal-randVal)/randVal)*100.0
    print "BASELINE BRANCH IS",(baselineB/(bmax*1.0))*100.0,"% OF MAX COVERAGE FOR ANY RUN"
       
    

f1 = plt.figure(figsize=(5,2))

plt.ylabel("Branches covered")

plt.xlim(0.5,3.5)

plt.xticks(xrange(0,8),("","random","LOC","swarm","LOC\n+swarm","GA","LOC\n+GA"))

bb = plt.boxplot([data["random"]["branch"],data["LOC"]["branch"],data["swarm"]["branch"],data["LOC+swarm"]["branch"],data["GA"]["branch"],data["LOC+GA"]["branch"]],manage_xticks=False)

x1, y1 = [2.5, 2.5], plt.axis()[2:]
plt.plot(x1, y1,color='black')

x1, y1 = [4.5, 4.5], plt.axis()[2:]
plt.plot(x1, y1,color='black')


pp = PdfPages("covbranch.pdf")

pp.savefig(f1)
pp.close()


f1 = plt.figure(figsize=(5,2))

plt.ylabel("Statements covered")

plt.xlim(0.5,3.5)

plt.xticks(xrange(0,8),("","random","LOC","swarm","LOC\n+swarm","GA","LOC\n+GA"))

bb = plt.boxplot([data["random"]["stmt"],data["LOC"]["stmt"],data["swarm"]["stmt"],data["LOC+swarm"]["stmt"],data["GA"]["stmt"],data["LOC+GA"]["stmt"]],manage_xticks=False,showmeans=True,meanline=True)

x1, y1 = [2.5, 2.5], plt.axis()[2:]
plt.plot(x1, y1,color='black')

x1, y1 = [4.5, 4.5], plt.axis()[2:]
plt.plot(x1, y1,color='black')


pp = PdfPages("covstmt.pdf")

pp.savefig(f1)
pp.close()


if anyFailed:
    
    f1 = plt.figure(figsize=(8,2))

    plt.ylabel("Failed tests")

    plt.xlim(0.5,3.5)

    plt.xticks(xrange(0,8),("","random","LOC","swarm","LOC\n+swarm","GA","LOC\n+GA"))

    bb = plt.boxplot([data["random"]["fail"],data["LOC"]["fail"],data["swarm"]["fail"],data["LOC+swarm"]["fail"],data["GA"]["fail"],data["LOC+GA"]["fail"]],manage_xticks=False,showmeans=True,meanline=True)

    x1, y1 = [2.5, 2.5], plt.axis()[2:]
    plt.plot(x1, y1,color='black')

    x1, y1 = [4.5, 4.5], plt.axis()[2:]
    plt.plot(x1, y1,color='black')


    pp = PdfPages("covfail.pdf")

    pp.savefig(f1)
    pp.close()
