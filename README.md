# Wikidata Qualifier Analysis Tools

## Contents

src: tools for importing a wikidata copy and computing the quaifier usage frequencies and diversity indexes

stats: results of the stat computation for different versions of wikidata

classification: qualifier categorization and analysis work (in xlsx files)


## Analysis process

1. Download a wikidata copy. For instance

    nohup curl -C - https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2 -o latest-all.json.bz2 &

   (wait for ~ 12 hours)

2. Extract the {qualifier -> {property -> frequency}}, the {qualifier -> frequency}, and the {property -> frequency} dictionaries

    bzip2 -dkc latest-all.json.bz2 | python3.9 <path-to>/src/import/extract-p-q-matrix.py >extract.out &

  (wait for ~ 12 hours)

  This gnerates three files: mat-p-q.json, q-count.json, and p-count.json.

3. Extract the property names :
   
   use the wikidata query service with the query in src/import/import_property_labels.sparql

   download in json and sort the file ("sort by" in sparql causes a timout)

   sort -u prop-names-25.json > prop-names.json
   
   edit prop-names.json to add a , to the line that was in last position and remove it from the last line

4. Generate a browser friendly version of the q->p->frequenciesdictionary (with the qualifier and property names)

    python3 path-to/src/import/present_p_q.py mat-p-q.json q-count.json prop-names.json >present-p-q-freq.json

5. Compute the diversity indexes

    python3 <path-to>/src/import/diversity_index.py mat-p-q.json q-count.json p-count.json. prop_names.json >q_diversity.csv

6. Use q_diversity and present-p-q-freq.json to analyze the qualifiers