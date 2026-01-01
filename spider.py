"""
spider.py
---------
Crawls a single website, extracts links between pages,
and stores page/link relationships in an SQLite database.

This script is intentionally limited to one domain
to ensure ethical crawling.
"""

import sqlite3
import urllib.request
import urllib.parse
import ssl
from bs4 import BeautifulSoup

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Database setup
conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.executescript('''
CREATE TABLE IF NOT EXISTS Pages (
    id INTEGER PRIMARY KEY,
    url TEXT UNIQUE,
    html TEXT,
    error INTEGER,
    old_rank REAL,
    new_rank REAL
);

CREATE TABLE IF NOT EXISTS Links (
    from_id INTEGER,
    to_id INTEGER,
    UNIQUE(from_id, to_id)
);

CREATE TABLE IF NOT EXISTS Webs (
    url TEXT UNIQUE
);
''')

# Load allowed websites
webs = []
cur.execute('SELECT url FROM Webs')
for row in cur:
    webs.append(row[0])

while True:
    cur.execute('''
        SELECT id, url FROM Pages
        WHERE html IS NULL AND error IS NULL
        ORDER BY RANDOM() LIMIT 1
    ''')
    row = cur.fetchone()

    if row is None:
        start_url = input('Enter starting URL (or blank to quit): ')
        if not start_url:
            break

        cur.execute('INSERT OR IGNORE INTO Webs (url) VALUES (?)', (start_url,))
        cur.execute('''
            INSERT OR IGNORE INTO Pages (url, html, old_rank, new_rank)
            VALUES (?, NULL, 1.0, 1.0)
        ''', (start_url,))
        conn.commit()
        continue

    from_id, url = row
    print(f'Retrieving: {url}')

    cur.execute('DELETE FROM Links WHERE from_id=?', (from_id,))

    try:
        response = urllib.request.urlopen(url, context=ctx)
        if response.getcode() != 200:
            cur.execute('UPDATE Pages SET error=? WHERE url=?', (response.getcode(), url))
            conn.commit()
            continue

        if 'text/html' not in response.getheader('Content-Type', ''):
            cur.execute('UPDATE Pages SET error=-1 WHERE url=?', (url,))
            conn.commit()
            continue

        html = response.read()
    except Exception:
        cur.execute('UPDATE Pages SET error=-1 WHERE url=?', (url,))
        conn.commit()
        continue

    cur.execute('UPDATE Pages SET html=? WHERE url=?', (html, url))
    conn.commit()

    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('a')

    for tag in tags:
        href = tag.get('href')
        if href is None:
            continue

        href = urllib.parse.urljoin(url, href)
        href = href.split('#')[0]

        if href.endswith(('.png', '.jpg', '.gif')):
            continue

        if webs:
            if not any(href.startswith(web) for web in webs):
                continue

        cur.execute('INSERT OR IGNORE INTO Pages (url, old_rank, new_rank) VALUES (?, 1.0, 1.0)', (href,))
        cur.execute('SELECT id FROM Pages WHERE url=?', (href,))
        to_id = cur.fetchone()[0]

        cur.execute('INSERT OR IGNORE INTO Links (from_id, to_id) VALUES (?, ?)', (from_id, to_id))

    conn.commit()

print('Crawling complete')
