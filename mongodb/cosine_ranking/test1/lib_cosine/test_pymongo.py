
import sys, os
projectpath = os.path.dirname(os.path.realpath('idf_storage.py'))
libpath = projectpath + '/lib_cosine'
sys.path.append(libpath)
os.chdir(projectpath)


import parsing_cosine as parsing
import re
import time
import pymongo
from pymongo import MongoClient

from pprint import pprint
# Indexing
startTime = time.time()
index = {}



# database collection settings
import CommonNames as CN

client = MongoClient()
db = CN.getDatabase(client)
index_col_name = CN.indexCollectionName()
tfvectDoc_col_name = CN.tfvCollectionName()
document_col_name = CN.documentCollectionName()


# ==============================

cursor = db[index_col_name].find()

docs= {}

for document in cursor:
    d = document['info']['document(s)']
    d2 = list(document['info']['document(s)'].keys())
    # print(document)
    print(d)

    for element in d2:
        if element not in docs:
            docs[element] = {}

        docs[element][document['_id']] = d[element]['frequency']


    # print(d2)
    # print("=======")



# pprint(docs)

e = 'a'
d = 'b'

# db['test'].insert_one({
#     e: {
#         d: 'frequency'
#     }
# })
#
# db['test'].insert_one({
#     '_id': 'werweiru82398jewjd',
#     '_tf': [{'a':12312},{'c':12312},{'b':12312}]
# })

tt = db.test.find_one({'_id' : 'werweiru82398jewjd'})
list = list(tt['_tf'])

list.append({'m':546456})

tt['_tf'] = list

print (list)

db['test'].update_one(
    {'_id':tt['_id']},
    {
        "$set":{
            '_tf': list
        }
    }
)








