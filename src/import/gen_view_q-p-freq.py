"""
Create a json file from a Q -> (P -> nb stmt) dictionary that is suitable for presentation
in a json-capable web browser
- the qualifiers are ordered by descreasing frequency (nb. of statements)
- for a qualifier the properties are ordered by decreasing frequency
- URI are added to provide a one-click access to the property definitions

usage: python present_p_q.py qualifier-property-frequency.json qualifier-freq.json prop-names.json
"""
import json
import sys

sbpbq = json.load(open(sys.argv[1]))
pname = json.load(open(sys.argv[3]))
sbq = json.load(open(sys.argv[2]))


print('{')
firstq = ''
for q in sorted(list(sbpbq.keys()), key = lambda x : sbq[x], reverse = True):
    print(firstq)
    firstq = ','
    qname = pname[q].replace('"','\\"') if q in pname else '*** UNKNOWN NAME '+q
    print(f""""{sbq[q]:.>9} {q} {qname}": {{"{qname}": "https://www.wikidata.org/wiki/Property:{q}" """)
    first = ','
    for p in sorted( list(sbpbq[q].keys()), key = lambda x : sbpbq[q][x], reverse=True):
        pn  = pname[p].replace('"','\\"') if p in pname else '*** UNKNOWN NAME '+p
        print(f"""{first} "{p:.<6}.{sbpbq[q][p]:.>9}  {pn}": "https://www.wikidata.org/wiki/Property:{p}" """)
        first = ','
    print('}')
print('}')