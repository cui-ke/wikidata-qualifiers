"""
Compute the diversity indexes for the qualifiers

output: for each qualifier several diversity indexes 
    currently:
        - the Shannon diversity index
        - the normalized Shannon index
        
    For a qualifier Q, 
    
        Shannon(Q) = Sum_{Pi \in P}{f(Q, Pi)/s(Q) * log(f(q, Pi)/s(Q))}
        
        where 
        - f(Q, Pi) is the frequency of Q in statements with predicate Pi
        - s(Q) is the sum of the F(Q, Pi) over all the Pi's
        
        ShannonNorm(Q) = Sum_{Pi \in P}{f(Q, Pi)/f(Pi)/sn(Q) * log(f(q, Pi)/f(Pi)/sn(Q))}
        
        where
        - f(Pi) is the number of statement with predicate Pi
        - sn(Q) is the sum of the F(Q, Pi)/f(Pi) over all the Pi's
"""
import json
import sys
import math

PROP_NAMES = 'property_names.json'
STMT_BY_PROP = 'stmtByProperty.json'
STMT_BY_QUAL = 'stmtByQualifier.json'
STMT_BY_PQ = 'stmtByPropertyByQualifier.json'

with open(PROP_NAMES) as pnmf :
    pname = json.load(pnmf)

with open(STMT_BY_PROP) as fpf :
    fp = json.load(fpf)

with open(STMT_BY_QUAL) as fqf :
    fq = json.load(fqf)

with open(STMT_BY_PQ) as fpqf :
    f = json.load(fpqf)

divsh = {}
divshn = {}

for q in f:
    sq = sum(f[q].values())
    snq = 0
    for p in f[q]: 
        snq += f[q][p]/fp[p]
    shan = 0.0
    shannorm = 0.0
    sumtp = 0.0
    sumtpn = 0.0
    for p in f[q]: 
        tp = f[q][p]/sq
        shan +=  tp * math.log(tp)
        sumtp += tp
        tpn = f[q][p]/fp[p]/snq
        shannorm += tpn * math.log(tpn)
        sumtpn += tpn
    idx = math.exp(-shan)
    idxn = math.exp(-shannorm)
    divsh[q] = idx
    divshn[q] = idxn

for q in sorted(list(fq.keys()), key = lambda x : fq[x], reverse=True):
    name = pname[q] if q in pname else "*** UNKNOWN NAME"
    name = name.replace('"','""')
    print(f'{q},"{name}",{fq[q]},{divsh[q]},{divshn[q]}')
