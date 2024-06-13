"""
Compute the #predicate/#qualifer for the properties

output: for each qualifier several diversity indexes 
    currently:
        - the Shannon diversity index
        - the normalized Shannon index
        

"""
import json
import sys
import math
import csv

PROP_NAMES = 'property_names.json'
STMT_BY_PROP = 'stmtByProperty.json'
STMT_BY_QUAL = 'stmtByQualifier.json'

with open(PROP_NAMES) as pnmf :
    pname = json.load(pnmf)

with open(STMT_BY_PROP) as fpf :
    fp = json.load(fpf)

with open(STMT_BY_QUAL) as fqf :
    fq = json.load(fqf)

# csvo = open('ratios.csv','w')

cw = csv.writer(sys.stdout)

for prop in pname:
    nqual = fq[prop] if prop in fq else 0
    npred = fp[prop]  if prop in fp else 0
    if nqual + npred > 0:
        cw.writerow([prop, pname[prop], nqual/(nqual+npred), nqual, npred])

