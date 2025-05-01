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

    bzip2 -dkc latest-all.json.bz2 | python3.9 <path-to>/src/import/extract_q-p-freq.py >extract.out &

  (wait for ~ 12 hours)

  This gnerates three files: q-p-freq.json, q-freq.json, and p-freq.json.

3. Extract the property names :
   
   use the wikidata query service with the query in src/import/import_property_labels.sparql

   download in json and sort the file ("sort by" in sparql causes a timout)

   sort -u prop-names-25.json > prop-names.json
   
   edit prop-names.json to add a , to the line that was in last position and remove it from the last line

4. Generate a browser friendly version of the q->p->frequenciesdictionary (with the qualifier and property names)

    python3 path-to/src/import/gen_view_q-p-freq.py q-p-freq.json q-freq.json prop-names.json >view_q-p-freq.json

5. Compute the diversity indexes

    python3 <path-to>/src/import/diversity_index.py q-p-freq.json q-freq.json p-freq.json. prop_names.json >q_diversity.csv

6. Use q_diversity.csv and present-q-p-freq.json to analyze the qualifiers