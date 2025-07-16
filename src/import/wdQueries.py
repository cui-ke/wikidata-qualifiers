
import json
import sys
import csv


from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict

from pathlib import Path

def get_prop_names():
    file_path = Path("prop-names.csv")  # File in current directory   
    if file_path.exists():
        print("Get property names from 'prop-names.csv'", file=sys.stderr)
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            pnames = {}
            for row in reader:
                if row:  # Skip empty rows
                    pnames[row[0]] = row[1]
        return pnames
    else:
        # Set up the SPARQL endpoint
        print("Get property names from query.wikidata.org/sparql", file=sys.stderr)
        endpoint_url = "https://query.wikidata.org/sparql"
        sparql = SPARQLWrapper(endpoint_url)
        wdprefix = 'http://www.wikidata.org/entity/'
        
        # Define the SPARQL query
        query = """
        SELECT DISTINCT ?item ?itemLabel 
            WHERE 
            {
            ?item wikibase:claim ?p
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # Helps get the label in your language, if not, then en language
            }
        """
        
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        
        try:
            # Execute the query and convert to Python dict
            results = sparql.query().convert()
            
            # Create the p -> {allowed qualifiers} dictionary

            pnames = {}

            for result in results["results"]["bindings"]:
                p = result["item"]["value"].replace(wdprefix,'')
                pname = result["itemLabel"]["value"].replace(wdprefix,'')
                pnames[p] = pname
            
            print(f"Found {len(pnames)} properties with their names", file=sys.stderr)
            pnfile = open("prop-names.csv","w")
            
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for p, name in pnames.items():
                    writer.writerow([p, name])
            print(f"Property -> Name saved to {file_path}",file=sys.stderr)

            return pnames
            
        except Exception as e:
            print(f"Error while querying Wikidata for property names: {e}", file=sys.stderr)
            return {}


def get_qualifier_constraints():
    file_path = Path("prop-allowed-qualifiers.json")  # File in current directory   
    if file_path.exists():
        print("Get allowed as qualifiers from 'prop-allowed-qualifiers.json'", file=sys.stderr)
        allowedq_list = json.load(open("prop-allowed-qualifiers.json"))
        return {key : set(value) for key, value in allowedq_list.items()}
    else:    
        print("Get allowed as qualifiers from 'query.wikidata.org/sparql'", file=sys.stderr)
        # Set up the SPARQL endpoint
        print("Get allowed as qualifiers from wikidata", file=sys.stderr)
        endpoint_url = "https://query.wikidata.org/sparql"
        sparql = SPARQLWrapper(endpoint_url)
        wdprefix = 'http://www.wikidata.org/entity/'
        
        # Define the SPARQL query
        query = """
        SELECT ?p ?q
        {  
            ?p wikibase:qualifier ?pq . # select all properties
            ?p p:P2302 ?sc . 
            ?sc ps:P2302 wd:Q21510851 .  
            ?sc pq:P2306 ?q 
        }
        """
        
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        
        try:
            # Execute the query and convert to Python dict
            results = sparql.query().convert()
            
            # Create the p -> {allowed qualifiers} dictionary

            allowedq = {}

            for result in results["results"]["bindings"]:
                p = result["p"]["value"].replace(wdprefix,'')
                q = result["q"]["value"].replace(wdprefix,'')
                if p not in  allowedq : 
                    allowedq[p] = set([q])
                else:
                    allowedq[p].add(q)
            
            print(f"Found {len(allowedq)} properties with qualifier constraints", file=sys.stderr)
            allowedq_list = {key: list(value) for key, value in allowedq.items()}

            json.dump(allowedq_list, open("prop-allowed-qualifiers.json","w"))
            print("Property -> Allowed Qualifiers saved to file",file=sys.stderr)
            return allowedq
            
        except Exception as e:
            print(f"Error while querying Wikidata for allowed qualifier constraints: {e}", file=sys.stderr)
            return {}

def get_allowed_as_qualifier():
    # Set up the SPARQL endpoint

    file_path = Path("allowed-as-qualifiers.csv")  # File in current directory
    
    if file_path.exists():
        print("Get allowed as qualifiers from 'allowed-as-qualifiers.csv'", file=sys.stderr)
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            qualifiers = set()
            for row in reader:
                if row:  # Skip empty rows
                    qualifiers.add(row[0])  # Add first (and only) column value
        return qualifiers
    else:
        print("Get allowed as qualifiers from 'https://query.wikidata.org/sparql'", file=sys.stderr)
        endpoint_url = "https://query.wikidata.org/sparql"
        sparql = SPARQLWrapper(endpoint_url)
        wdprefix = 'http://www.wikidata.org/entity/'
        
        # Define the SPARQL query
        query = """
            SELECT DISTINCT ?p 
                {
                ?p wikibase:qualifier ?q . # only look for qualifiers
                OPTIONAL { ?p p:P2302 ?sc . ?sc ps:P2302 wd:Q53869507 .  # property scope consraint
                        MINUS { ?sc pq:P5314 wd:Q54828449 . } # not allowing qualifiers
                        MINUS { ?sc pq:P4680 ?scope . } # no scope for this Constraint
                        MINUS { ?sc wikibase:rank wikibase:DeprecatedRank . } # not deprecated
                        BIND ( "NO" as ?allowed ) } # not allowed as qualifier
                FILTER(! BOUND(?allowed))   
                }
        """
        
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        
        try:
            # Execute the query and convert to Python set
            results = sparql.query().convert()
            
            qualifiers = set()

            for result in results["results"]["bindings"]:
                p = result["p"]["value"].replace(wdprefix,'')            
                qualifiers.add(p)
            
            print(f"Found {len(qualifiers)} properties allowed as qualifiers", file=sys.stderr)
            return qualifiers
            
        except Exception as e:
            print(f"Error while querying Wikidata for properties allowed as qualifiers: {e}", file=sys.stderr)
            return {}




# Execute the functions to produce JSON results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == '--names':
            pnames = get_prop_names()
            print(json.dumps(pnames, indent=4))
        elif cmd == '--aqconstraints':
            allowedq = get_qualifier_constraints()
            print(json.dumps(allowedq, indent=4))
        elif cmd == '--asqualifiers':
            asq = get_allowed_as_qualifier()
            for p in asq : 
                print(p)
