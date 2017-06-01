from whoosh import highlight
from whoosh.index import open_dir
from whoosh.query import Phrase, Term, spans
from whoosh.highlight import SentenceFragmenter
from nltk import ngrams
from bs4 import BeautifulSoup
import codecs, collections, subprocess, urllib.request


class CustomScorer(highlight.FragmentScorer):
    def __init__(self, phrase):
        # Get the list of words from the phrase query
        self.words = phrase.words

    def __call__(self, f):
        # Create a dictionary mapping words to the positions the word
        # occurs at, e.g. "foo" -> [1, 5, 10]
        d = collections.defaultdict(list)
        for token in f.matches:
            d[token.text].append(token.pos)

        # For each position the first word appears at, check to see if the
        # rest of the words appear in order at the subsequent positions
        firstword = self.words[0]
        for pos in d[firstword]:
            found = False
            for word in self.words[1:]:
                pos += 1
                if pos not in d[word]:
                    break
            else:
                found = True

            if found:
                return 100
        return 0


# One can search this index in many ways. Let's read in the novel Tom Jones
# and see which  trigrams from that file appear in any of our indexed files.
'''response = urllib2.urlopen("http://www.gutenberg.org/cache/epub/6593/pg6593.txt")
html = response.read().decode('utf-8')

with codecs.open("tom_jones.txt","w","utf-8") as tom_jones_out:
	tom_jones_out.write(html)'''

with codecs.open("tom_jones.txt", "r", "utf-8") as tom_jones_in:
    tom_jones_trigrams = ngrams(
        tom_jones_in.read().replace("\r", "").replace("\n", " ").split("PROJECT GUTENBERG")[1].split(
            "PROJECT GUTENBERG")[0].split(), 3)

with codecs.open("matching_searches.txt", "w", "utf-8") as matching_searches_out:
    ix = open_dir("index_for_sample_files")
    with ix.searcher() as searcher:
        for trigram in tom_jones_trigrams:

            phrase_query = Phrase("full_text", trigram)
            results = searcher.search(phrase_query)
            results.fragmenter.charlimit = None
            results.scorer = CustomScorer(phrase_query)
            for hit in results:

                # We've identified at least one hit in our index. Whoosh contains a built-in
                # set of tools we can use to "highlight" those hits, but we can also grep the
                # files with hits to extract the matching string in context
                file_with_hit = hit["path"]
                author_of_hit_file = hit["author"]
                title_of_hit_file = hit["short_title"]

                with codecs.open(hit["path"], "r", "utf-8") as fileobj:
                    filecontents = fileobj.read()
                    hit_highlights = hit.highlights("full_text", text=filecontents, top=100000)

                    # A single hit highlights object can contain multiple hits separated by an ellipsis.
                    # Make sure you get them all:
                    hit_list = BeautifulSoup(hit_highlights).get_text().split("...")
                    for hit in hit_list:
                        clean_hit = "..." + " ".join(x for x in hit.split()) + "..."

                        matching_searches_out.write(u" ".join(x for x in
                                                              trigram) + "\t" + author_of_hit_file + "\t" + title_of_hit_file + "\t" + file_with_hit + "\t" + clean_hit + "\n")