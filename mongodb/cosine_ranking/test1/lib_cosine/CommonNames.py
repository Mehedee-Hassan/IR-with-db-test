
def getDatabase(client):
    return client.Crime_News_DB

def indexCollectionName():
    return 'index'


def documentCollectionName():
    return 'documents'


def tfvCollectionName():
    return 'tf_doc_vector'