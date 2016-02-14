import sqlite3
import sys

from tabulate import tabulate

from func import *


if len(sys.argv) == 1:
    print('''Searcher 3000

Usage:
    python2 search.py <query>
    ''')
    sys.exit(1)

search_query = sys.argv[1]

conn = sqlite3.connect("lab.db")
db = conn.cursor()

words = extract_words(search_query)

words_ids = []
for word in words:
    word_id = get_word_id(db, word.lower())
    if not word_id:
        print ("results for %s not found" % word)
        continue

    words_ids.append(word_id)

summary_urls_ids = []
summary_scores = []
summary = {}

for word_id in words_ids:
    urls_ids = get_distinct_url_id_by_word_id(db, word_id)

    for url_id in urls_ids:
        url_id = url_id[0]
        if url_id in summary:
            summary[url_id] += 1
        else:
            summary[url_id] = 1

urls_ids = summary.keys()
urls_score = summary.values()

for i in range(len(urls_score)):
    for j in range(len(urls_score)-1-i):
        if urls_score[j] < urls_score[j+1]:
            urls_score[j], urls_score[j+1] = urls_score[j+1], urls_score[j]     # Swap!
            urls_ids[j], urls_ids[j+1] = urls_ids[j+1], urls_ids[j]

urls = []
for url_id in urls_ids:
    url = get_url_by_id(db, url_id)
    urls.append(url)


table = []
for index, url in enumerate(urls, 0):
    table.append([url, urls_score[index]])

print(tabulate(table, ["URL", "Score"]))
