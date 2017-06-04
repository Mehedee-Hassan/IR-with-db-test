import sys, os

projectpath = os.path.dirname(os.path.realpath('console_main.py'))
libpath = projectpath + '/lib_cosine'
sys.path.append(libpath)
os.chdir(projectpath)



from pymongo import MongoClient
import querying_cosine as qur





# Connect to the database containing inverted indexes
client = MongoClient()
db = client.Inverted_Index
# Choose a folder containing documents
folder = 'New Testament'
collection = db[folder]


class browser():
    def __init__(self, parent=None):
       pass

    def query(self):
        # Empty the list
        # Get the words in the query

        text = input("search:")

        words = qur.cleanQuery(text)

        # Collect the information for each word of the query
        index = {}
        for word in words:
            index[word] = collection.find({'_id': word})[0]['info']
        # Rank the documents according to the query
        results = qur.rankDocuments(index, words)
        for result in results:
            print(result[0] + ' : ' + str(round(result[1], 2)))


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
