from math import log, sqrt
from snowballstemmer import FrenchStemmer as fs
from nltk.corpus import stopwords
import re

def cleanQuery(string):
    frenchStopWords = stopwords.words('english')
    p = re.compile('\w+')
    words = p.findall(string)
    words = [word.lower() for word in words]
    words = [fs().stemWord(word) for word in words]
    words = [word for word in words if word not in frenchStopWords]
    return words





def rankDocuments(index, words ,numberOfDocuments):
    # We rank each document based on query


    queryTfVector = queryDocTFcalc(words)

    # unique terms
    words = set(words)

    # document that has terms in query
    doclist = {}



    rankings = {}


    for word in words:

        for document in index[word]['document(s)'].keys():

            # Term Frequency (log to reduce document size scale effect)
            TF = index[word]['document(s)'][document]['frequency']
            DF = index[word]['document frequency']
            doc_id = index[word]['document(s)'][document]['doc_id']


            if TF > 0:
                TF = 1 + log(TF)
            else:
                TF = 0


            idf = numberOfDocuments / DF
            idf = log(idf ,10)

            tfidf = TF * idf



            # Store scores in the ranking dictionary
            if document not in rankings:
                rankings[document] = TF


                # document that this term

            else:
                rankings[document] += TF

            if doc_id not in doclist:
                doclist[doc_id] = []

            doclist[doc_id].append((word ,tfidf))




    ranklist = normalizedVector(doclist,queryTfVector)



    # Order results according to the scores
    rankings = list(reversed(sorted(rankings.items(), key=lambda x: x[1])))

    ranklist = ((sorted(ranklist.items(), key=lambda x: x[1])))

    return ranklist

    

#  calculating normalization and cosine distance
def normalizedVector(doclist,queryTfVector):

    doc_ids = doclist.keys()

    print(len(doc_ids))


    ranking = {}

    sumofsq = 0
    for id in doc_ids:

        for element in doclist[id]:
            sumofsq += element[1]*element[1]

        sq = sqrt(sumofsq)

        temp_vector = {}

        for element in doclist[id]:
            temp_vector[element[0]] = element[1]/sq


        cosineValue = 0
        for key,value in temp_vector.items():

            cosineValue += temp_vector[key] * queryTfVector[key]

        ranking[id] = cosineValue


    return ranking



def queryDocTFcalc(words):

    temp_vect = {}
    for w in words:

        if w not in temp_vect:
            temp_vect[w] = 1

        else:
            temp_vect[w] += 1

    return queryDocNorm(temp_vect)


def queryDocNorm(temp_vect):


    sum = 0
    for key ,value in temp_vect.items():

        if value > 1:
           value = 1+log(value,10)



        sum += value*value


    sq = sqrt(sum)

    tmp = {}
    for key ,value in temp_vect.items():
        tmp[key] = temp_vect[key]/sq


    return tmp




