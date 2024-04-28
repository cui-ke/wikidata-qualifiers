""" 
Wikidata dump transposer

input: a NT RDF wikidata dump

output: a set of files, one for each property or qualifier
   a triple sss http://www.wikidata.org/prop/Pxxx ooo is writen into p/Pxxx.nt
                http://www.wikidata.org/prop/statement/Pxxx          ps/Pxxx.nt
                http://www.wikidata.org/prop/qualifier/Pxxx          pq/Pxxx.nt 
                
GF 2021-22
"""

import sys
import re

schema = 'http://schema.org/'

rdfs = 	'http://www.w3.org/2000/01/rdf-schema#'

p = 'http://www.wikidata.org/prop/P'
ps = 'http://www.wikidata.org/prop/statement/P'
pq = 'http://www.wikidata.org/prop/qualifier/P'
pr = 'http://www.wikidata.org/prop/reference/P'
prov = "http://www.w3.org/ns/prov#"
wd = "http://www.wikidata.org/entity/Q"
wds = "http://www.wikidata.org/entity/statement/"
wdref = "http://www.wikidata.org/reference/"

def select(ln: str)  :
  """
  checks if the line (triple) contains a p:..., ps:..., pq:... property
  or and rdfs:label property with a string in English   
  """
  if ln.find(p) > -1 : return True
  if ln.find(ps) > -1 : return True
  if ln.find(pq) > -1 : return True
  if ln.find(pr) > -1 : return True
  if ln.find(prov) > -1 : return True
  if ln.find(rdfs+"label") > -1 and ln.find("@en") > -1 : return True
  return False

lc = 0
ls = 0


for line in sys.stdin:
    # print(line)
    lc = lc + 1
    if select(line) : 
        ls = ls + 1
        
        # extract the property name
        
        triple = line.split(" ")
        prop = triple[1]
        
        # the property prefix (cat) will determine the output file directory
        
        cat = 'other'
        if prop.startswith('<'+rdfs+"label") : cat = 'label'
        if prop.startswith('<'+p) : cat = 'p'
        if prop.startswith('<'+ps) : cat = 'ps'
        if prop.startswith('<'+pq) : cat = 'pq'
        if prop.startswith('<'+pr) : cat = 'pr'
        if prop.startswith('<'+prov) : cat = 'prov'
        
        pname = "UNKNOWN"
        if cat == 'label' : pname = 'label'
        elif cat == 'prov' : pname = 'wasDerivedFrom'
        elif cat == 'other' : pname = 'allProps'
        else: 
            pmatch = re.search('/(P[0-9]+)>', prop)
            if pmatch != None: 
                pname = pmatch.group(1)
             
        # compress the Line, replace IRIs by prefix:name
        
        line = re.sub('<'+p+'([^>]+)>', r'p:P\1', line)
        line = re.sub('<'+ps+'([^>]+)>', r'ps:P\1', line)
        line = re.sub('<'+pq+'([^>]+)>', r'pq:P\1', line)
        line = re.sub('<'+pr+'([^>]+)>', r'pr:P\1', line)
        line = re.sub('<'+prov+'([^>]+)>', r'prov:P\1', line)
        
        line = re.sub('<'+wd+'([^>]+)>', r'wd:Q\1', line)
        line = re.sub('<'+wds+'([^>^/]+)>', r'wds:\1', line)
        line = re.sub('<'+wdref+'([^>^/]+)>', r'wdref:\1', line)
                
        fo = open('triples/' + cat + '/' + pname + '.nt','a')
        fo.write(line)
        fo.close
        
        # print(line)
        if ls % 100000 == 0 : 
            print(str(ls//1000)+'k triples  ('+str(lc//1000)+'k lines)')    
    # -- end if
# -- end for
