import sys, os
projectpath = os.path.dirname(os.path.realpath('idf_storage.py'))
libpath = projectpath + '/lib_cosine'
sys.path.append(libpath)
os.chdir(projectpath)
import parsing_cosine as parsing
import re
import time

# Indexing
startTime = time.time()
index = {}
# What collection to index?
collection = 'dailystar'
files_collection = "documents"


# Indicate the path where relative to the collection
os.chdir(projectpath + '/data/' + collection)
# os.chdir(projectpath + '/data_temp/')


# os.chdir(projectpath + '/data/' + files_collection)
# List all files in the collection
files = [file for file in os.listdir('.') if os.path.isfile(file)]
# Iterate through every file
for file in files:
    # Split the file in lines

    temp_doc = open(file).read()
    data = temp_doc.splitlines()
    # Normalize the content
    words = parsing.clean(data)
    # Remove the extension from the file for storage
    name = re.match('(^[^.]*)', file).group(0)

    id = parsing.store_doc(files_collection, temp_doc)

    # Add the words to the index
    parsing.index(name, words, index,id)




print("Indexation took " + str(time.time() - startTime) + " seconds.")

# Storage
startTime = time.time()
parsing.store(index, collection)
print("Storage took " + str(time.time() - startTime) + " seconds.")
