# Extract the property-qualifier matrix from a wikidata json dump

"""
input: a wikidata json dump (in std input)
output: 
    p-q-frequ.json
        on each line : <property> : {<qualifier>: <frequency>, ...}
    p-freq.json
        on each line : <property>: <frequency>
    q-freq.json
        on each line : <qualifier>: <frequency>

usage: bzip2 -cdk wikidata-dump.json.bz2 | python path-to-extract-p-q-freq.py

"""

import sys
import json

def writedict(f, dico):
    fo = open(f, 'w')
    lc = 0
    fo.write('{\n')
    for k in dico:
        lc += 1
        fo.write(f'  "{k}": {json.dumps(dico[k])}')
        if lc < len(dico) : fo.write(',')
        fo.write('\n')
    fo.write('}\n')
    fo.close()

pcount = {}
qcount = {}
mat = {}
ci = 0 # line count

for line in sys.stdin:
    if len(line) > 2:
        ci += 1
        if ci % 1000 == 0 : print(f"{ci:,}")
        ls = line.strip()
        while ls[-1] != '}' : ls = ls[:-1]
        j = json.loads(ls)
        # print(j['id'])

        claims = j["claims"] if "claims" in j else {}

        for p in claims:
            if p not in mat : mat[p] = {}
            if p not in pcount : pcount[p] = 0
            pcount[p] += len(claims[p])
            for claim in claims[p]:
                if "qualifiers" in claim:
                    qualifs = claim["qualifiers"]                
                    for q in qualifs:
                        if q not in qcount : qcount[q] = 0
                        qcount[q] += 1 # += len(qualifs[q]) to count the total #occ of each qualifier
                        if q not in mat[p] : mat[p][q] = 0
                        mat[p][q] += 1 # += len(qualifs[q]) to count the total #occ of each qualifier

print('writing results')
writedict('p-q-freq.json',mat)
writedict('p-freq.json', pcount)
writedict('q-freq.json', qcount)



