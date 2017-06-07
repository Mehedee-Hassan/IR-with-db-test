
import sys, os
from pprint import pprint

projectpath = os.path.dirname(os.path.realpath('idf_storage.py'))
libpath = projectpath + '/lib_cosine'
sys.path.append(libpath)
os.chdir(projectpath)


import parsing_cosine as parsing
import re
import time
import pymongo
from pymongo import MongoClient
import math

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
def if_exists(collection,data):
    t= (collection.find({'_id':data}).count())
    print(t)
    if t>0:
        return True
    else:
        return False

def TFVectorForDoc():

    cursor = db[index_col_name].find()
    db[tfvectDoc_col_name].count()

    docs = {}

    for document in cursor:
        d = document['info']['document(s)']
        d2 = list(document['info']['document(s)'].keys())

        for doc_id_as_key in d2:


            #  if document exists in tf_doc_vector

            if if_exists(db[tfvectDoc_col_name], doc_id_as_key) == False:

                # insert in to tfdocvector

                db[tfvectDoc_col_name].insert_one({
                    '_id': doc_id_as_key,
                    '_tf': {document['_id']:d[doc_id_as_key]['frequency']}
                })


            #  if document doesnt exist in the tf_doc_vector
            else:
                try:
                    # get the list of tf

                    tf_list = ((db[tfvectDoc_col_name].find_one({'_id': doc_id_as_key})))

                    tf_list = (tf_list['_tf'])

                    # pprint(tf_list)
                    # append new object to old one
                    tf_list[document['_id']] = d[doc_id_as_key]['frequency']

                    # pprint(tf_list)

                    # update collection

                    db[tfvectDoc_col_name].update_one(
                        {'_id': doc_id_as_key},
                        {
                            "$set": {
                                '_tf': tf_list
                            }
                        }
                    )

                except:
                    print("null")

              # docs[doc_id_as_key][document['_id']] = d[doc_id_as_key]['frequency']



def saveNormalization():
    data = db[tfvectDoc_col_name].find()

    for element in data:

        pprint(element)
        sumtf = 0
        for tf in element['_tf'].items():

            # pprint(tf)
            # pprint(tf[1])

            sumtf += (tf[1]*tf[1])


        print(sumtf)
        sq = math.sqrt(sumtf)



        normlist = {}

        for tf in element['_tf'].items():

            tempNorm = tf[1]/sq
            normlist[tf[0]] = tempNorm

        try:


            # update collection

            db[tfvectDoc_col_name].update_one(
                {'_id': element['_id']},
                {
                    "$set": {"_normtf":normlist}
                }


            )

        except:
            print("null")


 # save normalized vector for each document's words


TFVectorForDoc()

# save normalized vector for each document's words
saveNormalization()