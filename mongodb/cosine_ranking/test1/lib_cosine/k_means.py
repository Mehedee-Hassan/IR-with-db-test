
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






def returnVect(documentID):

    tf_list = db[tfvectDoc_col_name].find_one({'_id': documentID})
    tf_list = dict(tf_list['_normtf'])

    return tf_list




def cosine_distance(doc1 ,doc2
                    # avg_vect,avg_count_vect
                    ,vect1
                    ,vect2
                    ,__emptyVect):



    if __emptyVect == True:
        vect1 = (returnVect(doc1))
        vect2 = (returnVect(doc2))




    distance =0
    summationV = []
    # pprint(vect1)

    sum_v = 0

    for word,val in vect1.items():


        # mean vector save
        # if word not in avg_vect:
        #     avg_vect[word] = 0
        #     avg_count_vect[word] =0
        #
        #
        # avg_vect[word] += val
        # avg_count_vect[word] +=1

        if word in vect2:
            sum_v += (vect1[word]*vect2[word])



    return sum_v


def main():

    avg_vect = {}
    avg_count_vect = {}
    distance = cosine_distance('5935b4b55b65ad41a0817765','5935b4b55b65ad41a0817767',
    avg_vect,
    avg_count_vect)


    # print (avg_vect)
    print ("distance = ",distance)

# main()




ClusterA = 1
ClusterB = 2


def k_means(document_list):
    first_mean = document_list[0]
    second_mean = document_list[len(document_list)-1]

    cluster = {}

    avg_vect = {}
    avg_count_vect = {}

    __emptyVect = True

    meanA={}
    meanB={}


    oldA = {}
    oldB = {}
    oldCluster = {}

    while True:

        for doc in document_list:


            distance1 = cosine_distance(doc , first_mean
                                        ,meanA
                                        ,meanB
                                        ,__emptyVect)

            distance2 = cosine_distance(doc , second_mean
                                        ,meanA
                                        ,meanB
                                        ,__emptyVect)

            if distance1 > distance2:
                cluster[doc] = ClusterA
            else:
                cluster[doc] = ClusterB



        meanA ,meanB = avg_vector(cluster)


        _changeFlag = cluserChanged(cluster,oldCluster)

        if _changeFlag == False:
            break


        oldCluster = cluster


        __emptyVect = False

    for key,val in cluster.items():
        print("doc = ",key,'cluster= ',val)




def cluserChanged(cluster,oldCluster):

    if len(oldCluster) <=0:
        return True

    for key,val in cluster.items():
        if cluster[key] != oldCluster[key]:
            return True


    return False







def avg_vector(cluser):

    meanCluserA = {}
    meanCluserACnt = {}

    meanCluserB = {}
    meanCluserBCnt = {}


    print("k means 1 " ,"cluster = ",cluser)

    for key ,val in cluser.items():

        if val  == ClusterA:
            word_vector = returnVect(key)

            for word ,tfnorm in word_vector.items():

                if word not in meanCluserA:
                    meanCluserA[word] = 0
                    meanCluserACnt[word] = 0

                print("k_means2" , word ," transform",tfnorm)

                meanCluserA[word] += float(tfnorm)
                meanCluserACnt[word] += 1

        if val  == ClusterB:
            word_vector = returnVect(key)

            for word ,tfnorm in word_vector.items():

                if word not in meanCluserB:
                    meanCluserB[word] = 0
                    meanCluserBCnt[word] = 0

                meanCluserB[word] += tfnorm
                meanCluserBCnt[word] += 1


        for key ,val in meanCluserA.items():
            meanCluserA[key] = meanCluserA[key] / meanCluserACnt[key]

        for key ,val in meanCluserB.items():
            meanCluserB[key] = meanCluserB[key] / meanCluserBCnt[key]

    return meanCluserA,meanCluserB