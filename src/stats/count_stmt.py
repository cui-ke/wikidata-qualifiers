# Count the number of statements

"""
input: a wikidata json dump (in std input)
output: results in count_stmt.out

usage: bzip2 -cdk wikidata-dump.json.bz2 | python <path-to-count_stmt.py>
"""

import sys
import json

fo = open('count_stmt.out','w')

stmt_c = 0
stmt_with_q_c = 0
entity_c = 0

for line in sys.stdin:
    if len(line) > 2:
        ls = line.strip()
        while ls[-1] != '}' : ls = ls[:-1]
        entity = json.loads(ls)
        entity_c += 1
        # print(entity['id'])

        claims = entity["claims"] if "claims" in entity else {}

        for p in claims:
            stmt_c += len(claims[p])
            for stmt in claims[p]:
                if "qualifiers" in stmt:
                    if len(stmt["qualifiers"]) > 0 :
                        stmt_with_q_c += 1                
                    
        if entity_c % 1000 == 0:
            fo.write(f'e: {entity_c:_}, stmt: {stmt_c:_}, qualified: {stmt_with_q_c:_}, {stmt_with_q_c/stmt_c*100:8.4f}\n')
            fo.flush()

fo.write(f'e: {entity_c}, stmt: {stmt_c}, qualified: {stmt_with_q_c}, {stmt_with_q_c/stmt_c*100}\n')
fo.close()