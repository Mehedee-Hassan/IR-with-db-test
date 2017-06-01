from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StandardAnalyzer
from string import  punctuation
# import string.maketrans

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import codecs, sys, glob, os, unicodedata

# Define stopwords using NLTK standard stopword list for English language
stopset = set(stopwords.words('english'))

# Load unicode punctuation
tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                    if unicodedata.category(chr(i)).startswith('P'))


# Create function with which to strip punct from unicode
def remove_punctuation(unicode_text):
    return unicode_text.translate(tbl)


# Make the index folder
if not os.path.exists("index_for_sample_files"):
    os.mkdir("index_for_sample_files")

# Specify a list of paths that contain all of the texts we wish to index
text_dirs = ["sample_text_collection"]

# Create metadata dict
metadata_dict = {}
with codecs.open("sample_text_collection_metadata.txt", "r", "utf-8") as metadata_in:
    metadata_rows = metadata_in.read().split("\n")
    for row in metadata_rows[:-1]:
        split_row = row.split("\t")
        filename = split_row[0].strip()
        author = split_row[1].strip()
        short_title = split_row[2].strip()

        if filename not in metadata_dict.keys():
            metadata_dict[filename] = {}
            metadata_dict[filename]["author"] = author
            metadata_dict[filename]["short_title"] = short_title


# Create function that will allow one to retrieve metadata fields for a given filename
def retrieve_metadata(filename):
    if filename in metadata_dict.keys():
        return metadata_dict[filename]
    else:
        return None
        print("no metadata for: ", filename)


# Identify the schema we'll use when creating index
schema = Schema(filename=TEXT(stored=True), path=TEXT(stored=True), author=TEXT(stored=True),
                short_title=TEXT(stored=True),
                full_text=TEXT(stored=True, phrase=True, analyzer=StandardAnalyzer(stoplist=None)))

# Create the index using the schema
ix = create_in("index_for_sample_files", schema)

writer = ix.writer()

for i in text_dirs:
    for j in glob.glob(i + "/*.txt"):
        with codecs.open(j, "r", "utf-8") as raw_file:
            cleaner_file = remove_punctuation(raw_file.read().replace("\r", "").replace("\n", " "))

            # Grab filename, then use that to grab all metadata. NB: Unix users should change the following line to j.split("/")[-1]
            filename = j.split("\\")[-1]
            print ("indexing file: ", filename)

            path = j.decode("utf-8")
            file_metadata = retrieve_metadata(filename)
            author = file_metadata["author"].decode("utf-8")
            short_title = file_metadata["short_title"].decode("utf-8")

            # Now push full text and metadata fields to the index
            writer.add_document(filename=unicode(filename), path=path, author=author, short_title=short_title,
                                full_text=cleaner_file)

# Commit changes to index
writer.commit()