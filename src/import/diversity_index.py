"""
Compute the diversity indexes for the qualifiers

usage:

    python3 diversity_index.py q-p-freq.json q-freq.json p-freq.json prop-names.json

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
from wdQueries import get_prop_names

# PROP_NAMES = sys.argv[4] # 'property_names.json'
PROP_FREQ = sys.argv[3] # 'stmtByProperty.json'
QUAL_FREQ = sys.argv[2] # 'stmtByQualifier.json'
Q_P_FREQ = sys.argv[1] # 'stmtByPropertyByQualifier.json'

#with open(PROP_NAMES) as pnmf :
#    pname = json.load(pnmf)
pname = get_prop_names()

with open(PROP_FREQ) as fpf :
    fp = json.load(fpf)

with open(QUAL_FREQ) as fqf :
    fq = json.load(fqf)

with open(Q_P_FREQ) as fqpf :
    f = json.load(fqpf)

divsh = {}
divshn = {}
abundance = {}

for q in f:
    abundance[q] = len(f[q]) # abundance
    sum_prop_freq = sum(f[q].values()) # Sum of the frequencies of the properties qualified by q
    sum_proportional_prop_freq = 0
    # Sum of the proportional frequencies of the properties qualified by q
    for p in f[q]: 
        sum_proportional_prop_freq += f[q][p]/fp[p]
    shan = 0.0
    shanprop = 0.0
    # sumtp = 0.0
    # sumtpn = 0.0
    for p in f[q]: 
        relative_freq_of_p = f[q][p]/sum_prop_freq 
        shan +=  relative_freq_of_p * math.log(relative_freq_of_p)
        # sumtp += relative_freq_of_p
        relative_proportional_freq_of_p = f[q][p]/fp[p]/sum_proportional_prop_freq
        shanprop += relative_proportional_freq_of_p * math.log(relative_proportional_freq_of_p)
        # sumtpn += relative_proportional_freq_of_p
    idx = math.exp(-shan)
    idxn = math.exp(-shanprop)
    divsh[q] = idx
    divshn[q] = idxn

print(f'Qualifer,Name,Frequency,Sh. Diversity,Sh. Prop. Diversity,Abundance,Importance Score')
for q in sorted(list(fq.keys()), key = lambda x : divshn[q]*fq[x], reverse=True):
    if q in f:
        name = pname[q] if q in pname else "*** UNKNOWN NAME"
        name = name.replace('"','""')
        print(f'{q},"{name}",{fq[q]},{divsh[q]},{divshn[q]}, {abundance[q]}, {divshn[q]*fq[q]}')
