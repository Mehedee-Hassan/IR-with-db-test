#!python3
"""
https://whoosh.readthedocs.io/en/latest/quickstart.html
Whoosh Quick Start

create index

results:
E:\scratch\qs1 is created.
_MAIN_0.toc file is created in the directory, 
maybe, a binary file with size less than 2kb.
"""

import os
from whoosh.index import create_in
#from whoosh.fields import *
from whoosh.fields import Schema, TEXT, ID

indexdir = 'scratch\qs1'

if not os.path.exists(indexdir):
    os.mkdir(indexdir)
    
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
ix = create_in(indexdir, schema)

