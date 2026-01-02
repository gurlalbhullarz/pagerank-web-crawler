import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('''
SELECT Pages.id, Pages.url, Pages.new_rank, COUNT(Links.to_id) AS inbound
FROM Pages JOIN Links ON Pages.id = Links.to_id
GROUP BY Pages.id
ORDER BY new_rank DESC
''')

count = input('How many nodes to visualize: ')
count = int(count) if count.isdigit() else 20

nodes = list()
links = list()

rows = cur.fetchmany(count)
node_ids = [row[0] for row in rows]

min_rank = min(row[2] for row in rows)
max_rank = max(row[2] for row in rows)

for row in rows:
    nodes.append({
        "id": row[0],
        "label": row[1],
        "value": (row[2] - min_rank) / (max_rank - min_rank + 0.0001)
    })

cur.execute('SELECT from_id, to_id FROM Links')
for row in cur:
    if row[0] in node_ids and row[1] in node_ids:
        links.append({"source": row[0], "target": row[1]})

with open('spider.js', 'w') as f:
    f.write('var nodes = ' + str(nodes) + ';\n')
    f.write('var links = ' + str(links) + ';\n')

print('spider.js created')
