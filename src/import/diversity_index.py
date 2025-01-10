"""
Compute the diversity indexes for the qualifiers

usage:

    python3 diversity_index.py q_p_freq.json q_freq.json p_freq.json prop_names.json

output: for each qualifier several diversity indexes 
    currently:
        - the Hill number of order 1, which is exp(Shannon diversity index)
        - the proportional Hill number of order 1, which is exp(Shannon diversity index)
           on the proportional frequencies of the properties
        
    For a qualifier Q, 
    
        Shannon(Q) = Sum_{Pi \in P}{f(Q, Pi)/s(Q) * log(f(q, Pi)/s(Q))}
        
        where 
        - f(Q, Pi) is the frequency of Q in statements with predicate Pi
        - s(Q) is the sum of the f(Q, Pi) over all the Pi's
        
        ShannonProp(Q) = Sum_{Pi \in P}{f(Q, Pi)/f(Pi)/sn(Q) * log(f(q, Pi)/f(Pi)/sn(Q))}
        
        where
        - f(Pi) is the number of statement with predicate Pi
        - sn(Q) is the sum of the F(Q, Pi)/f(Pi) over all the Pi's
"""
import json
import sys
import math

PROP_NAMES = sys.argv[4] # 'property_names.json'
PROP_FREQ = sys.argv[3] # 'stmtByProperty.json'
QUAL_FREQ = sys.argv[2] # 'stmtByQualifier.json'
Q_P_FREQ = sys.argv[1] # 'stmtByPropertyByQualifier.json'

with open(PROP_NAMES) as pnmf :
    pname = json.load(pnmf)

with open(PROP_FREQ) as fpf :
    fp = json.load(fpf)

with open(QUAL_FREQ) as fqf :
    fq = json.load(fqf)

with open(Q_P_FREQ) as fqpf :
    f = json.load(fqpf)

divsh = {}
divshn = {}

for q in f:
    sq = sum(f[q].values())
    snq = 0
    for p in f[q]: 
        snq += f[q][p]/fp[p]
    shan = 0.0
    shanprop = 0.0
    sumtp = 0.0
    sumtpn = 0.0
    for p in f[q]: 
        tp = f[q][p]/sq
        shan +=  tp * math.log(tp)
        sumtp += tp
        tpn = f[q][p]/fp[p]/snq
        shanprop += tpn * math.log(tpn)
        sumtpn += tpn
    idx = math.exp(-shan)
    idxn = math.exp(-shanprop)
    divsh[q] = idx
    divshn[q] = idxn

for q in sorted(list(fq.keys()), key = lambda x : fq[x], reverse=True):
    name = pname[q] if q in pname else "*** UNKNOWN NAME"
    name = name.replace('"','""')
    print(f'{q},"{name}",{fq[q]},{divsh[q]},{divshn[q]}')
