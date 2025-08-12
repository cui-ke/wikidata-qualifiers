# Count the number of statements

"""
input: a wikidata json dump (in std input)
output:
 - no. non-deprecated statements
 - no. deprecated stmts
 - no. non-deprecated, non-example stmts
 - no. qualified statements
 - no. qualified statements that are not examples

usage: bzip2 -cdk wikidata-dump.json.bz2 | python path-to-count_stmt.py
"""

import sys
import json

fo = open('count_stmt.out','w')

stmt_count = 0 # non-dep statements
dep_stmt_count = 0
qualified_stmt_count = 0
entity_count = 0
qualified_count = 0
non_ex_qualified = 0
exclude = set(["P5977","P6685","P1855","P2271","P5192","P5193"])

for line in sys.stdin:
    if len(line) > 2:
        ls = line.strip()
        while ls[-1] != '}' : ls = ls[:-1]
        entity = json.loads(ls)
        entity_count += 1
        # print(entity['id'])

        claims = entity["claims"] if "claims" in entity else {}

        for p in claims:
            for claim in claims[p]:
                if "type" in claim and claim["type"] ==  "statement":
                    
                    if "rank" in claim and claim["rank"] == "deprecated":
                        dep_stmt_count += 1
                    else:
                        stmt_count += 1
                        if "qualifiers" in claim:
                            qualified_count += 1
                            if p not in exclude :
                                non_ex_qualified += 1
                                      
        if entity_count % 1000 == 0:
            fo.write(f'e: {entity_count:_}, s: {stmt_count:_}, ds: {dep_stmt_count}, qualified_count: {qualified_count:_} non_ex_qualified {non_ex_qualified:_}\n')
            fo.flush()

fo.write(f'e: {entity_count:_}, s: {stmt_count:_}, ds: {dep_stmt_count}, qualified_count: {qualified_count:_} non_ex_qualified {non_ex_qualified:_}\n')
fo.close()
