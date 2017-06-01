import os
from whoosh.index import create_in
# from whoosh.fields import *
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.index import open_dir



indexdir = 'scratch'

if not os.path.exists(indexdir):
    os.mkdir(indexdir)

schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
ix = create_in(indexdir, schema)





ix = open_dir(indexdir)

writer = ix.writer()
writer.add_document(title=u'First document', path=u'/a', content=u"This is the first document we've added!")
writer.add_document(title=u'First2 document', path=u'/b', content=u"This is the first nn document we've added!")
writer.add_document(title=u'Second document', path=u'/c', content=u'The second one is even more kuttA interesting!')
writer.add_document(title=u'Second2 document', path=u'/d', content=u'The second one is even more kuttA interesting!')
writer.add_document(title=u'Second3 document', path=u'/e', content=u'The second one is even more kuttA interesting!')
writer.commit()




ix = open_dir(indexdir)

with ix.searcher() as searcher:
    query = QueryParser('content', ix.schema).parse('nn  first')
    results = searcher.search(query)
    print(results)
    print(len(results))
    print(results[0])
    # print(results[1])
