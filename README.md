# Wikidata Qualifier Analysis Tools

## Contents

src: tools for importing a wikidata copy and computing the quaifier usage frequencies and diversity indexes

stats: results of the statistics computation for different versions of wikidata

classification: qualifier categorization and analysis work (in xlsx files)


## Analysis process

1. Download a wikidata copy. For instance

    nohup curl -C - https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2 -o latest-all.json.bz2 &

   (wait for ~ 12 hours)

2. Extract the {qualifier -> {property -> frequency}}, the {qualifier -> frequency}, and the {property -> frequency} dictionaries

    lbzip2 -dkc latest-all.json.bz2 | python3 <path-to>/src/import/extract_q-p-freq.py >extract.out &
  
  - lbzip2 is much faster than bzip2
  - most of the compute time is spent in lbzip2 => useless to optimize the python script
  - the script skips the deprecated statements
  
  (wait for ~3 hours (~ 12 hours with bzip2))

  This gnerates three files: p-q-freq.json, q-freq.json, and p-freq.json.

    python3 <path-to>/src/import/transpose_rmex_p_q.py <p-q-freq.json >q-p-freq.json # or transpose_p_q.py

  Generate the q-p-f by transposing p-q-f
  The rmex version removes the Wikidata example ... properties (not a real qualification use)


3. Extract the property names :
   
   use the wikidata query service with the query in src/import/import_property_labels.sparql

   download in json and sort the file ("sort by" in sparql causes a timout)

   sort -u prop-names-25.json > prop-names.json
   
   edit prop-names.json to add a , to the line that was in last position and remove it from the last line

4. Generate a browser friendly version of the q->p->frequenciesdictionary (with the qualifier and property names)

    #- JSON
    python3 path-to/src/import/gen_view_q-p-freq.py q-p-freq.json q-freq.json prop-names.json >view_q-p-freq.json
    #- HTML
    python3 path-to/src/import/gen_html_view.py q-p-freq.json q-freq.json prop-names.json >view_q-p-freq.html

    To obtain a view that shows the Allowed qualifiers constraint violation.
    a. Generate a csv file with the allowed qualifiers for each property (properties without constraint must not appear)

    SELECT ?p ?q
    {  ?p wikibase:qualifier ?pq . # select all properties
       ?p p:P2302 ?sc . ?sc ps:P2302 wd:Q21510851 .  ?sc pq:P2306 ?q 
    }

    b. Run gen_html_view.py with this file as last parameter

5. Generate the list of globally allowed qualifiers
   
   Theese are properties that are not explicitly dissalowed as qualifiers

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

6. Compute the diversity indexes

    python3 <path-to>/src/import/diversity_index.py q-p-freq.json q-freq.json p-freq.json. prop_names.json >q_diversity.csv

7. Use q_diversity.csv and view_q-p-freq.html to analyze the qualifiers