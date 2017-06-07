from snowballstemmer import FrenchStemmer as fs
from nltk.corpus import stopwords
import re
from pymongo import MongoClient


# database collection settings
import CommonNames as CN

client = MongoClient()
db = CN.getDatabase(client)
index_col_name = CN.indexCollectionName()
document_col_name = CN.documentCollectionName()


# ==============================




englishStopWords = stopwords.words('english')
p = re.compile('\w+')

def clean(data):
    # Concatenate the lines into a big string
    words = [word for word in ' '.join(data).split(' ')]
    # Search every word in the big string
    words = p.findall(' '.join(words))
    # Lower case
    words = [word.lower() for word in words]
    # Stem word
    # words = [fs().stemWord(word) for word in words]
    # Remove stop words
    words = [word for word in words if word not in englishStopWords]
    # Done!
    return words

def index(file, words, index, id):

    doc_id = str(id)

    for position in range(len(words)):
        word = words[position]     

        # If the word is not in the index
        if words[position] not in index:

            index[word] = {
                           # 'term frequency' : 1,
                           'document frequency' : 1,
                           'document(s)' : {doc_id : {'frequency' : 1,
                                                    # 'position(s)' : [position],
                                                    'doc_id'    : id
                                                      }
                                            }
                           }
        # If the word is in the index
        else:
            # index[word]['term frequency'] += 1
            # If the word has not been found in this document
            if doc_id not in index[word]['document(s)']:
                index[word]['document frequency'] += 1
                index[word]['document(s)'][doc_id] = {'frequency' : 1,
                                                      # 'position(s)' : [position],
                                                    'doc_id': id
                                                      }
            # If the word has been found in this document
            else:
                 index[word]['document(s)'][doc_id]['frequency'] += 1
                 # index[word]['document(s)'][file]['position(s)'].append(position)


    return index

def store(index, index_col_name):
    collection = db[index_col_name]


    for word in index:
        collection.save({'_id' : word, 'info' : index[word]})
    


def store_doc(files_collection,text):

    collection = db[files_collection]
    id = collection.save({'data':text})
    print (id)

    return id


