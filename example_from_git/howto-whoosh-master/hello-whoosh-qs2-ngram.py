#!python3
"""
https://whoosh.readthedocs.io/en/latest/quickstart.html
Whoosh Quick Start

same content as qs1, but with a schema NGRAM

results:
<Top 1 Results for And([Term('content', 'firs'), Term('content', 'irst')]) runti
me=0.001133428193173593>
1
<Hit {'title': 'First document', 'path': '/a'}>

4-gram? firs and irst.

the 2nd run shows same results.
means, create_in clears existing documents.
"""

import os
from whoosh.index import create_in
#from whoosh.index import open_dir
#from whoosh.fields import *
from whoosh.fields import Schema, NGRAM, ID
from whoosh.qparser import QueryParser

indexdir = r'scratch\qs2'

if not os.path.exists(indexdir):
    os.mkdir(indexdir)
    
schema = Schema(title=NGRAM(stored=True), path=ID(stored=True), content=NGRAM)
ix = create_in(indexdir, schema)
#ix = open_dir(indexdir)

writer = ix.writer()
writer.add_document(title=u'First document', path=u'/a', content=u"This is the first document we've added!")
writer.add_document(title=u'Second document', path=u'/b', content=u'The second one is even more kuttA interesting!')
writer.commit()

with ix.searcher() as searcher:
    query = QueryParser('content', ix.schema).parse('kutta')
    results = searcher.search(query)
    print(results)
    print(len(results))
    for result in results:
        print(result)
