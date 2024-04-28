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

print("""
@prefix p: <http://www.wikidata.org/prop/> .
@prefix : <http://cui.unige.ch/isi/wikidatamsl/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

""")

for p in fp:
    print(f'p:{p} :stmt_pred_count {fp[p]} .')
for p in pname:
    print(f'p:{p} rdfs:label "{pname[p]}" .')
for p in fq:
    print(f'p:{p} :stmt_qualified_count {fq[p]} .')

for q in f:
    for p in f[q]:
        # print(f'p:{q} :qualifies p:{p}.')
        print(f'<< p:{q} :qualifies p:{p}>> :stmt_count {f[q][p]}.')









