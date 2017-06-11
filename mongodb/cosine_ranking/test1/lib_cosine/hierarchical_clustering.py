
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
import queue


clusters = {}

def hierarchical(doc_list):
    length = len(doc_list)

    distance_dic = localDistance(doc_list)

    pair_list = make_pair_init(distance_dic)



    makeCluster_old(distance_dic, doc_list)




def make_pair_init(distance_dic):

    pq = queue.PriorityQueue()



    for key,doc_dictionary in distance_dic:

        for id_key,distance in doc_dictionary:

            # first document id = key and id = document id_key
            # val = cosine distance between two document
            # NC = not a cluster
            pq.put((distance , key ,id_key,'NC'))



    return pq











def returnVect(documentID):

    tf_list = db[tfvectDoc_col_name].find_one({'_id': documentID})

    # print("not in list = ",documentID)



    tf_list = dict(tf_list['_normtf'])

    return tf_list




def cosine_distance(doc1 ,doc2,__emptyVect):




    if __emptyVect == True:

        print("doc2 = ")
        pprint(doc2)
        vect1 = (returnVect(doc1))
        vect2 = (returnVect(doc2))
        pprint(vect2)

    else:
        vect1 = (returnVect(doc1))
        vect2 = doc2


    distance =0
    summationV = []
    # pprint(vect1)

    sum_v = 0

    for word,val in vect1.items():
        if __emptyVect == True:
            print('key = ',word," ",val)


        if word in vect2:
            sum_v += round((vect1[word]*vect2[word]),3)

    return sum_v



def localDistance(doc_list):

        distance = {}
        lenght = len(doc_list)

        for i in range(0,lenght):
            for j in range(i+1 ,lenght):

                if doc_list[i] not in distance:
                    distance[doc_list[i]] = {}

                if doc_list[j] not in distance:
                    distance[doc_list[j]] = {}

                print('now =',i,' ',j)

                dist = cosine_distance(doc_list[i],doc_list[j],True)
                distance[doc_list[i]][doc_list[j]]=dist
                distance[doc_list[j]][doc_list[i]]=dist




        for key ,val in distance.items():
            distance[key] = ((sorted(val.items(), key=lambda x: x[1],reverse=True)))




        pprint(distance)

        return distance



# old unfinished make cluster


def makeCluster_old(distance, doc_list):

    max = 0.0

    temp_dict = {}
    taken = {}
    cluster = {}
    cls = 0
    lenght = len(doc_list)
    now  = {}

    cl = []

    for i in range(0, lenght):

        if cls not in cluster:
            cluster[cls] = {}
        if doc_list[i] in taken:
            taken[doc_list[i]] = {}


        cluster[cls][doc_list[i]] = 2
        taken[doc_list[i]][cls]  = 2

        now[doc_list[i]] = cls

        cl.append(cls)
        cls+=1


    b = 0
    while True:

        for i in range(0, lenght):

           if i != lenght-1 and cl[i]!=cl[i+1]:

               key = distance[doc_list[i]].keys()

               for k in key:
                   if cl[doc_list[i]] != cl[k]:

                       dist_key = list(distance.keys())[0]

                       if k == dist_key:
                           now[dist_key] = now[doc_list[i]]

                       else:


               print(key[0]," ", list(distance.keys())[0])




           print('now =', i, ' ', j)


        b += 1
        if b > 1000:
            break







