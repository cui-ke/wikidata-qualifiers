# Wikidata Qualifier Analysis Tools

Analysis process

1. download

    nohup curl https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2 >20250101.json.bz2

2. extract the property-qualifier matrix and the prop. and qualif. counts (don't forget the -k for keep)

    bzip2 -cdk 20250101.json.bz2 | python3.9 extract-p-q-matrix.py 

   
