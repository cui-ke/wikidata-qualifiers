import os 
import sys
import re
import csv
import time

"""
 this script count the number of occurrences of a given qualifier for each property
 usage: $ python3 getpropq.py qualifier

 1. scans the files Pxxx-qualifiers in stats/ 
      row format: predicat,qualifier,q-name,frequency
 2. for the properties not found in stats read the triples/p/Pxxx.nt file
 
 usage: $ python3.9 getpropqn-v2.py p1 p2 ... pk
 
 generates p1-is-qualifier-of.csv ... pk-is-qualifier-of.csv
"""

qualifiers = sys.argv[1:]
fff = [{} for x in range(len(qualifiers))]
sps = [set() for x in range(len(qualifiers))] # sps[i] statements with qualifier qualifers[i]
qualifs_of_stmt = {}

already_done = set()
pq_path = '/home/falquet/wikidata/stats'
pqfiles = os.listdir(pq_path)

# explore the qualifier files ([predicate -> qualifier])
# to find qualifiers

for pqf in pqfiles :
    if re.match(r'P[0-9]+-qualifiers.csv', pqf):
        already_done.add(pqf.replace('-qualifiers.csv','.nt'))
        predicate = pqf.replace('-qualifiers.csv','')
        # find this qualifier in the property->qualifier file
        with open(os.path.join(pq_path, pqf),'r') as f:
            fr = csv.reader(f)
            for pqrow in fr:
                for i in range(len(qualifiers)):
                    if pqrow[1] == qualifiers[i] :
                        fff[i][predicate] = int(pqrow[3])
                        print(f'found q = {qualifiers[i]} p = {predicate} => {fff[i][predicate]}')


for i in range(len(qualifiers)):  
    qualifier = qualifiers[i]              
    pf = open('/home/falquet/wikidata/triples/pq/'+qualifier+'.nt','r')

    np = 0
    print(f'Reading triples with qualifier {qualifier}')
    for triple in pf :
        sss = (triple.split(" "))[0]  # get the statement
        sps[i].add(sss)
        if sss in qualifs_of_stmt :
            qualifs_of_stmt[sss].add(i)
        else:
            qualifs_of_stmt[sss] = set([i])
        np = np+1
    print(str(np)+' triples read')

p_path = '/home/falquet/wikidata/triples/p'
files = os.listdir(p_path)

# begin check
sps2 = [set() for x in range(len(qualifiers))] # sps[i] statements with qualifier qualifers[i]

for stmt in qualifs_of_stmt :
    for j in qualifs_of_stmt[stmt]:
        sps2[j].add(stmt)

for j in   range(len(qualifiers)):
    print(f'{qualifiers[j]}: |sps| = {len(sps[j])}, |sps2| = {len(sps2[j])}')

# end check

print('Searching the p: files ... ')

nt = 0
nof = 0
ptime0 = time.process_time()
ftime0 = time.perf_counter()
nq = [0 for x in range(len(qualifiers))]
nqs = [0 for x in range(len(qualifiers))]
for file in files:   # for all the properties
    nof += 1
    if file not in already_done and re.match(r'P[0-9]+\.nt', file):

        f = open(os.path.join(p_path,file),'r')
        for x in range(len(qualifiers)):
            nq[x] = 0
            nqs[x] = 0
        for x in f:   # for all the statements with this property
            nt = nt+1
            if nt % 1000000 == 0 :
                ptime1 = time.process_time()
                ftime1 = time.perf_counter()
                print(f'{nt} lines, {nof} files in {ptime1-ptime0} -- {ftime1-ftime0}')
                ftime0 = ftime1
                ptime0 = ptime1
            
            st = (x.split(" "))[2]  # extract the object = the statement
            """
            for i in range(len(qualifiers)):  
                if st in sps[i] :
                    nq[i] = nq[i]+1
            """
            if st in qualifs_of_stmt:
                for j in qualifs_of_stmt[st] :
                    nqs[j] = nqs[j]+1
        f.close()        
        for i in range(len(qualifiers)):  
            ### if nq[i] != nqs[i] : print(f'**** error: {file} qualifier # {i} {nq[i]} != {nqs[i]}')
            if nqs[i] > 0 :
                fff[i][file.replace(".nt", "")] = nqs[i]
    else:
        print('skipping '+file)

print(' ')
print(str(nt)+' triples read')

# print the qualifiers with their english label
pnf = open('/home/falquet/wikidata/propnames.tsv','r')
propnames = {}
for ln in pnf:
   lns = ln.split("\t")
   propnames[lns[0]] = lns[1].strip()
   
for i in range(len(qualifiers)): 
    qualifier = qualifiers[i]
    fo = open('stats/'+qualifier+'-is-qualifier-of.csv','w')
    cwriter = csv.writer(fo)
    for f in fff[i]:
       print(f + '\t' + propnames.get(f,'*** unknown name') + '\t' + str(fff[i][f]) )
       cwriter.writerow([f, propnames.get(f,'*** unknown name'), qualifier, fff[i][f] ])
    fo.close()
     
