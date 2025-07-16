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

    python3 <<path-to>>/src/import/transpose_rmex_p_q.py < p-q-freq.json > q-p-freq.json # or transpose_p_q.py

  Generate the q-p-f by transposing p-q-f
  The rmex version removes the 'Wikidata example ...' properties (not a real qualification use)


3. Generate a browser friendly version of the q->p->frequencies dictionary (with the qualifier and property names)

    python3 path-to/src/import/gen_html_view.py q-p-freq.json q-freq.json >view_q-p-freq.html

  In addition this script generates the following files if they don't exist yet: 
  - prop-names.csv - property names
  - allowed-as-qualifiers.csv  - the properties that are not explicitly prohibited as qualifiers
  - prop-allowed-qualifiers.json - the qualifiers allowed for each property with such a restriction


4. Compute the diversity indexes

    python3 <<path-to>>/src/import/diversity_index.py q-p-freq.json q-freq.json p-freq.json  >q_diversity.csv

2. Use q_diversity.csv and view_q-p-freq.html to analyze the qualifiers