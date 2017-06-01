import codecs, urllib.request, os, time

# Specify the name of the directory in which we'll store the sample text collection
if not os.path.exists("sample_text_collection"):
    os.makedirs("sample_text_collection")

# Create a list of urls from which we'll extract full texts
urls_to_ping = ['http://www.gutenberg.org/files/829/829-0.txt', 'http://www.gutenberg.org/files/521/521-0.txt',
                'http://www.gutenberg.org/cache/epub/2160/pg2160.txt']

# Loop over those urls, collecting the text from each, and writing limited metadata fields to disk
with codecs.open("sample_text_collection_metadata.txt", "w", "utf-8") as metadata_out:
    for url in urls_to_ping:
        response = urllib.request.urlopen(url)
        html = response.read().decode('unicode_escape').encode('utf-8')

        # Extract metadata features from each file
        author_name = html.split("Author:")[1].replace("\r", "").split("\n")[0]
        text_title = html.split("Title:")[1].replace("\r", "").split("\n")[0]
        filename = url.split("/")[-1]
        metadata_out.write(filename + "\t" + author_name + "\t" + text_title + "\n")

        with codecs.open("sample_text_collection/" + filename, "w", "utf-8") as file_out:
            file_out.write(html)

        # Pause the script for 2 seconds to throttle the requests to Project Gutenberg
        time.sleep(2)



