import sqlite3

from func import *

conn = sqlite3.connect("lab.db")
db = conn.cursor()

urls = open('urls').read().splitlines()

for url in urls:
    url_id = get_url_id(db, url)
    if url_id:
        print("%s already scanned, skipping" % url)
        continue

    url_id = add_url(db, url)

    print("Scanning words on %s" % url)
    words = scan_words(url)

    if words:
        (added_words, binded_words) = add_and_bind_words(db, url_id, words)
        print("Added %d new words" % added_words)
        print("Binded %d words" % binded_words)

conn.commit()
conn.close()
