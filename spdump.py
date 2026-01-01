import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('''
SELECT Pages.url, COUNT(Links.to_id) AS inbound
FROM Pages JOIN Links ON Pages.id = Links.to_id
GROUP BY Pages.id
ORDER BY inbound DESC
LIMIT 20
''')

for inbound, url in cur:
    print(inbound, url)
