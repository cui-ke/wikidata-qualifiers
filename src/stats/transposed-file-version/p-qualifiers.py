import os 
import sys
import re
import csv

#this script  count the  prominance of qualifier per property
# usage: $ python3 getqn.py property

property = sys.argv[1]
pf = open('/home/falquet/wikidata/triples/p/'+property+'.nt','r')
qout = open('stats/'+property+'-qualifiers.csv','w')

sp = set() # all the statements that are an object of this property

ff = {}

print("Reading the stat/Pxxx-is-qualifier-of files to find", property)
statpath = '/home/falquet/wikidata/stats'
iqo_files = os.listdir('stats')
for file in iqo_files:
    if re.match(r'P[0-9]+-is-qualifier-of.csv', file):
        f=open(os.path.join(statpath,file),'r')
        reader = csv.reader(f)
        for row in reader:
            if row[0] == property:
                print('found in '+file)
                ff[row[2]] = row[3]  # 2 = property name, 3 = nb. of qualifications
                break
                

np = 0
print('Reading triples with property', property )
for k in pf :
    sss = (k.split(" "))[2]
    sp.add(sss)
    np = np+1
print(str(np)+' triples read')

q_path = '/home/falquet/wikidata/triples/pq'
files = os.listdir(q_path)



print('Searching the qualifier files ... ')

nt = 0
nfiles = 0
for file in files:   # for all the qualifiers
   if re.match(r'P[0-9]+\.nt', file):
        qualifier = file.replace(".nt", "")
        if qualifier in ff:
            print('already found in stat/'+qualifier)
        else:
            # print(file, end =" ")
            f=open(os.path.join(q_path,file),'r')
            nq = 0
            nfiles += 1
            for x in f:   # for all the statements with this qualifier
                nt = nt+1
                if nt % 1000000 == 0 :
                    print('\r'+str(nt), 'nfiles:', nfiles, end='')
                st = (x.split(" "))[0]  # extract the subject = the statement
                if st in sp :
                    nq = nq+1        
            f.close()
            if nq > 0 :
                ff[file.replace(".nt", "")] = nq
print(' ')        
print(str(nt)+' triples read')

# print the qualifiers with their english label
pnf = open('/home/falquet/wikidata/propnames.tsv','r')
propnames = {}
for ln in pnf:
   lns = ln.split("\t")
   propnames[lns[0]] = lns[1].strip()

qwriter = csv.writer(qout)
   
for f in ff:
   # print(f + '\t' + propnames.get(f,'*** unknown name') + '\t' + str(ff[f]) + '\t' + str((ff[f]*100.0)/np))
   qwriter.writerow([property,f,propnames.get(f,'*** unknown name'),ff[f]])

qout.close()

   
