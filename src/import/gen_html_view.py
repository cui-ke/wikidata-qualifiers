"""
Create an html file from a Q -> (P -> nb stmt) dictionary that is suitable for presentation and exploration

- the qualifiers are ordered by descreasing frequency (# occurrences in statements)
- for a qualifier the properties are ordered by decreasing frequency (# times this qualifier qualifies a stmt that has tis property)
- URI are added to provide a one-click access to the property definitions

Highlight the errors:
- Qualifiers not allowed as qualifier
- Qualifier is not allowed for this property (allowed qualifier constraint violation)

usage: 
python gen_html_view.py qualifier-property-frequency.json qualifier-frequency.json 

"""
import json
import sys
import csv


from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
from wdQueries import get_prop_names, get_qualifier_constraints, get_allowed_as_qualifier


allowedq = get_qualifier_constraints()
pname = get_prop_names()
aasqualif = get_allowed_as_qualifier()

sbpbq = json.load(open(sys.argv[1]))
sbq = json.load(open(sys.argv[2]))


print("""<html><body>""")
print("""<h1>Qualifier usage</h1>
         <ul>
            <li>Qualifiers in orange are not allowed as qualifier</li>
            <li>Properties in red => Qualifier is not allowed for this property (allowed qualifier constraint violation)</li>
        </ul>
""")
print("""<table>""")
print("""<tr><th>Frequency</th><th>Qualifer</th><th align='left'>Qualified Properties</th><tr>""")
firstq = ''
for q in sorted(list(sbpbq.keys()), key = lambda x : sbq[x], reverse = True):
    if len(set(sbpbq[q].keys()).difference(set(["P5977","P6685","P1855","P2271","P5192","P5193"]))) > 0 :
        # print(firstq)
        firstq = ','
        print("<tr>")
        print(f"<td valign='top' align='right'>{sbq[q]}</td>")
        
        qname = pname[q].replace('"','\\"') if q in pname else '*** UNKNOWN NAME '+q
        if q in aasqualif :
            pattr = ''
        else:
            pattr = "bgcolor = 'orange'"
        print(f"""<td valign='top' {pattr}><a href="https://www.wikidata.org/wiki/Property:{q}">_{q}</a></td>""")
        # print(f""""{sbq[q]:.>9} {q} {qname}": {{"{qname}": "https://www.wikidata.org/wiki/Property:{q}" """)
        
        print(f"<td><details><summary>_{qname}</summary><table>")
        first = ','
        for p in sorted( list(sbpbq[q].keys()), key = lambda x : sbpbq[q][x], reverse=True):
            pn  = pname[p].replace('"','\\"') if p in pname else '*** UNKNOWN NAME '+p
            if p in allowedq and q not in allowedq[p]:
                 attr = 'bgcolor="red"'
            else:
                attr =''
            #print(f"""{first} "{p:.<6}.{sbpbq[q][p]:.>9}  {pn}": "https://www.wikidata.org/wiki/Property:{p}" """)
            print(f"""<tr><td {attr}>{p}</td><td align="right">{sbpbq[q][p]}</td><td><a href="https://www.wikidata.org/wiki/Property:{p}">{pn}</a></td></tr>""")
            first = ','
        print("</table></td>")
        print("</tr>")
print('</table>')
print('</body></html>')