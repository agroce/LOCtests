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
            "nocovsampguided":"LOC(nocov)",
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
    data[v]["bugs"] = []      

allBugs = set([])
    
for f in glob.glob("*guided." + TIMEOUT + ".*.out")+glob.glob("exploit0*." + TIMEOUT + ".*.out"):
    fname = f.split(".")[0]
    if fname not in category:
        continue
    bugset = set([])
    for l in open(f):
        if "ERROR" in l:
            errText = l.split("<traceback")[0]
            print errText
            bugset.add(errText)
                    
    tdata = category[fname]
    
    allBugs |= bugset
    
    data[tdata]["bugs"].append(len(bugset))

print "THERE ARE",len(allBugs),"DISTINCT FAULTS"
    
for cat in data:
    print cat,len(data[cat]["bugs"])
    
for field in ["bugs"]:
    if "fail" in field and not anyFailed:
        continue
    print "="*60
    print field.upper()+":"
    for cat in ["LOC","LOC(nocov)","LOC(stat)","LOC(old)","random","swarm","GA","LOC+swarm","LOC+GA"]:
        if len(data[cat][field]) == 0:
            continue
        print "  "+cat+":",scipy.mean(data[cat][field]),scipy.std(data[cat][field])
        if cat != "LOC":
            try:
                sr = scipy.stats.mannwhitneyu(data[cat][field],data["LOC"][field])
                print "    vs. LOC:",sr
            except ValueError:
                pass
        if cat != "LOC(nocov)":
            try:
                sr = scipy.stats.mannwhitneyu(data[cat][field],data["LOC(nocov)"][field])
                print "    vs. LOC(nocov):",sr
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

f1 = plt.figure(figsize=(8,2))

plt.ylabel("Faults detected")
plt.grid(axis='y')

plt.xlim(0.5,3.5)
plt.xticks(xrange(0,8),("","random","LOC","swarm","LOC\n+swarm","GA","LOC\n+GA"))

ymaxval = max(data["random"]["bugs"] + data["LOC"]["bugs"] + data["swarm"]["bugs"] + data["LOC+swarm"]["bugs"] + data["GA"]["bugs"] + data["LOC+GA"]["bugs"])+0.5

print ymaxval

plt.ylim(0,ymaxval)

print "TOTAL # BUGS", len(allBugs)

#bb = plt.boxplot([data["LOC"]["bugs"],data["random"]["bugs"],data["LOC+swarm"]["bugs"],data["swarm"]["bugs"],data["LOC+GA"]["bugs"],data["GA"]["bugs"]],manage_xticks=False)
bb = plt.boxplot([data["random"]["bugs"],data["LOC"]["bugs"],data["swarm"]["bugs"],data["LOC+swarm"]["bugs"],data["GA"]["bugs"],data["LOC+GA"]["bugs"]],manage_xticks=False,meanline=True,showmeans=True,meanprops={"color":"green", "linestyle":"--","linewidth":3})

x1, y1 = [2.5, 2.5], [0, ymaxval]
plt.plot(x1, y1,color='black')

x1, y1 = [4.5, 4.5], [0, ymaxval]
plt.plot(x1, y1,color='black')

pp = PdfPages("faultplot.pdf")

pp.savefig(f1)
pp.close()
