import sqlite3
import urllib
import re
import pyquery


def extract_words(content):
    words = re.findall(r'\w+', content)
    return words


def scan_words(url):
    page_response = urllib.urlopen(url)
    page_html = page_response.read()

    html_query = pyquery.PyQuery(page_html)
    page_text = html_query('p').text()

    return extract_words(page_text)


def get_url_id(db, url):
    db.execute("SELECT ID FROM urls WHERE URL='%s'" % url)
    data = db.fetchone()
    if data:
        return data[0]
    return None

def get_url_by_id(db, url_id):
    db.execute("SELECT URL FROM urls WHERE ID=%d" % url_id)
    data = db.fetchone()
    if data:
        return data[0]
    return None

def add_url(db, url):
    db.execute("INSERT INTO urls VALUES(NULL, '%s')" % url)
    return db.lastrowid


def get_word_id(db, word):
    db.execute("SELECT ID FROM words WHERE CONTENT='%s'" % word)
    data = db.fetchone()
    if data:
        return data[0]
    return None


def add_word(db, word):
    db.execute("INSERT INTO words VALUES(NULL, '%s')" % word)
    return db.lastrowid

def bind_url_word(db, url_id, word_id):
    db.execute(
        'INSERT INTO urls_words VALUES(NULL, {}, {})'.format(
            url_id, word_id
        )
    )
    return db.lastrowid


def add_and_bind_words(db, url_id, words):
    added_words = 0
    binded_words = 0

    for word in words:
        word = word.lower()
        word_id = get_word_id(db, word)

        if not word_id:
            word_id = add_word(db, word)
            added_words += 1

        bind_url_word(db, url_id, word_id)
        binded_words += 1

    return (added_words, binded_words)



def get_distinct_url_id_by_word_id(db, word_id):
    db.execute(
        "SELECT DISTINCT URL_ID FROM urls_words WHERE WORD_ID=%s" % word_id
    )
    return db.fetchall()
