#!python3
"""
https://whoosh.readthedocs.io/en/latest/quickstart.html
Whoosh Quick Start

search

results:
<Top 2 Results for Term('content', 'first') runtime=0.0006359875374212412>
2
<Hit {'title': 'First document', 'path': '/a'}>
<Hit {'title': 'First document', 'path': '/a'}>

this indicates duplicate path can be sored ignoring the uniqueness of ID.
"""

from whoosh.index import open_dir
from whoosh.qparser import QueryParser

indexdir = 'scratch\qs1'

ix = open_dir(indexdir)

with ix.searcher() as searcher:
    query = QueryParser('content', ix.schema).parse('first')
    results = searcher.search(query)
    print(results)
    print(len(results))
    print(results[0])
    print(results[1])
