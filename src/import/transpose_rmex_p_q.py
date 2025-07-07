"""
Transpose: from Prop => (Qual => N) to Qual => (Propo => N)

Do not consider the "Wikidata Example ..." properties because their qualifiers are not "real" qualifiers

"""

import json
import sys


fi = sys.stdin
pqc = json.loads(fi.read())

exclude = set(["P5977","P6685","P1855","P2271","P5192","P5193"])

qpc = {}
for p in pqc:
    if p not in exclude:
        for q in pqc[p]:
            if q not in qpc : qpc[q] = {}
            qpc[q][p] = pqc[p][q]

print(json.dumps(qpc, indent=4))
