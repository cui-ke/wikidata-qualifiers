"""
Create an thml file from a Q -> (P -> nb stmt) dictionary that is suitable for presentation and exploration

- the qualifiers are ordered by descreasing frequency (nb. of statements)
- for a qualifier the properties are ordered by decreasing frequency
- URI are added to provide a one-click access to the property definitions

If a file with the allowed qualifiers is provided, highlight the errors = qualifiers that qualify a property
not allowing this qualifier. Each line of the file contains a property and an allowed qualifier. Properties
not appearing in the file have no qualifier constraints.

usage: 
python present_p_q.py qualifier-property-frequency.json qualifier-freq.json prop-names.json [allowed.csv]

"""
import json
import sys
import csv

sbpbq = json.load(open(sys.argv[1]))
pname = json.load(open(sys.argv[3]))
sbq = json.load(open(sys.argv[2]))

allowedq = {}
if len(sys.argv) > 4:
    with open(sys.argv[4], mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] not in  allowedq : 
                allowedq[row[0]] = set([row[1]])
            else:
                allowedq[row[0]].add(row[1])

# print(f"***{allowedq}") #chk

print("""<html><body>""")
print("""<table>""")
firstq = ''
for q in sorted(list(sbpbq.keys()), key = lambda x : sbq[x], reverse = True):
    if len(set(sbpbq[q].keys()).difference(set(["P5977","P6685","P1855","P2271","P5192","P5193"]))) > 0 :
        # print(firstq)
        firstq = ','
        print("<tr>")
        print(f"<td valign='top' align='right'>{sbq[q]}</td>")
        #print(f"<td valign='top'>_{q}</td>")
        qname = pname[q].replace('"','\\"') if q in pname else '*** UNKNOWN NAME '+q
        print(f"""<td valign='top'><a href="https://www.wikidata.org/wiki/Property:{q}">_{q}</a></td>""")
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