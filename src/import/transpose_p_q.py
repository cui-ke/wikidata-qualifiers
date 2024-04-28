"""
Transpose: from Prop => (Qual => N) to Qual => (Propo => N)
"""

import json
import sys


fi = sys.stdin
pqc = json.loads(fi.read())

qpc = {}
for p in pqc:
    for q in pqc[p]:
        if q not in qpc : qpc[q] = {}
        qpc[q][p] = pqc[p][q]

print(json.dumps(qpc))
