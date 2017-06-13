import sys, os



projectpath = os.path.dirname(os.path.realpath('console_main.py'))
libpath = projectpath + '/lib_cosine'
sys.path.append(libpath)
os.chdir(projectpath)
import CommonNames as CN


from pprint import  pprint
from pymongo import MongoClient
import temp_query_cosine as qur
from bson.objectid import ObjectId
import k_means
import hierarchical_clustering as hierarchical



# database collection settings
import CommonNames as CN

client = MongoClient()
db = CN.getDatabase(client)
index_col_name = CN.indexCollectionName()
document_col_name = CN.documentCollectionName()
tfvectDoc_col_name = CN.tfvCollectionName()


# ==============================




indexCollection = db[index_col_name]
documentCollection = db[document_col_name]

tf_docVector = db[tfvectDoc_col_name]


class browser():
    def __init__(self, parent=None):
       pass

    def query(self):
        # Empty the list
        # Get the words in the query

        text = input("search:")

        words = qur.cleanQuery(text)
        # words = set(words)


        print(words)
        # Collect the information for each word of the query
        index = {}
        for word in words:
            print(word +" ")

            try:

                index[word] = indexCollection.find({'_id': word})[0]['info']
                # print(index[word])

            except :
                print("not found")


        print('intex len =' ,tf_docVector.count())

        # Rank the documents according to the query
        results = qur.rankDocuments(index, words, db[document_col_name].count())


        tt = []

        for result in results:
            print(str(result[0]) + ' : ' + str((result[1])))

            print("============================")

            test = documentCollection.find_one({"_id": result[0]})

            # pprint(test)
            print("============XXX=============")


        doclist = [str(r[0]) for r in results]

        print("list == ",doclist,'\n  length = ',len(doclist))

        if len(doclist)!=0:
            # k_means.k_means(doclist)

            print("test")

            hierarchical.hierarchical(doclist)



def tf_search():
    myapp = browser()
    myapp.query()

def idf_search():
    pass


if __name__ == "__main__":

    # only tf ranking
    tf_search()

    # idf ranking
    # cosine distance calculating

    idf_search()
