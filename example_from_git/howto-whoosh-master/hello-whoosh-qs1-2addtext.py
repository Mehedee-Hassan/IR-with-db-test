#!python3
"""
https://whoosh.readthedocs.io/en/latest/quickstart.html
Whoosh Quick Start

add text document

results:
_MAIN_0.toc is renamed to _MAIN_1.toc.
two files are created; MAIN_WRITELOCK and MAIN_xxh7q0wfd37x562g.seg.
The last one has indexes.

the 2nd run results:
no errors shown though the path break the uniqueness to the 1st run.
now _MAIN_2.toc. 
maybe, overwrite the 1st one?
another seg file is created; MAIN_x1ec288ljfq1ffi4.seg.
size matched to the 1st one, but the binary comparing differs. 
"""

from whoosh.index import open_dir

indexdir = 'scratch\qs1'

ix = open_dir(indexdir)

writer = ix.writer()
writer.add_document(title=u'First document', path=u'/a', content=u"This is the first document we've added!")
writer.add_document(title=u'Second document', path=u'/b', content=u'The second one is even more kuttA interesting!')
writer.commit()

