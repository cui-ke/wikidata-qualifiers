# Count the number of statements

"""
input: a wikidata json dump (in std input)


usage: bzip2 -dk wikidata-dump.json.bz2 | python path-to-count_stmt.py
"""

import sys
import json

stmt_c = 0
stmt_with_q_c = 0
entity_c = 0

for line in sys.stdin:
    if len(line) > 2:
        ls = line.strip()
        while ls[-1] != '}' : ls = ls[:-1]
        entity = json.loads(ls)
        entity_c += 1
        # print(j['id'])

        claims = entity["claims"] if "claims" in j else {}

        for p in claims:
            stmt_c += len(claims[p])
            for stmt in claims[p]:
                if "qualifiers" in stmt:
                    if len(stmt["qualifiers"]) > 0 :
                        stmt_with_q_c += 1                
                    
        if entity_c % 10000 == 0:
            print(f'e: {entity_c}, stmt: {stmt_c}, qualified: {stmt_with_q_c}')




