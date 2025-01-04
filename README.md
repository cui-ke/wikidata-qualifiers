# Wikidata Qualifier Analysis Tools

Analysis process

1. download

    nohup curl https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2 >20250101.json.bz2

2. extract the property-qualifier matrix

    gunzip 20250101.json.bz2 | python extract-p-q-matrix.py 

   
