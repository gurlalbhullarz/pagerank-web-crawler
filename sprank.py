"""
sprank.py
---------
Computes PageRank values for crawled pages
using an iterative graph-based algorithm.
"""
import sqlite3
conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute("SELECT DISTINCT from_id FROM Links")
from_ids = list()
for row in cur:
    from_ids.append(row[0])
if len(from_ids) < 1:
    print("No links Found")
    quit()

links = list()
cur.execute('SELECT DISTINCT from_id, to_id FROM Links')
for row in cur:
    from_id = row[0]
    to_id = row[1]
    if from_id == to_id:
        continue
    if from_id not in from_ids:
        continue
    if to_id not in from_ids:
        continue
    links.append((from_id,to_id))
prev_ranks = dict()
cur.execute('SELECT id, old_rank FROM Pages')
for row in cur:
    prev_ranks[row[0]] = row [1]
many = input("How many iterations:")
if many.isdigit():
    many = int(many)
else:
    many = 1

for i in range(many):
    print(f'Iteration {i + 1}')
    next_ranks = dict()
    total = 0.0
    for node in prev_ranks:
        total+= prev_ranks[node]
        next_ranks[node] = 0.0
    for node in prev_ranks:
        old_rank = prev_ranks[node]
        give_ids = list()
        for link in links:
            if link[0] == node:
                give_ids.append(link[1])
        if len(give_ids) < 1:
            continue
        amount = old_rank / len(give_ids)
        for id in give_ids:
            next_ranks[id] += amount
    evap = (total - sum(next_ranks.values()))/len(next_ranks)
    for node in next_ranks:
        next_ranks[node] += evap
    diff = 0
    for node in prev_ranks:
        diff += abs(prev_ranks[node] - next_ranks[node])
    print('Average change:', diff / len(prev_ranks))
    prev_ranks = next_ranks
for node in prev_ranks:
    cur.execute(
            'UPDATE Pages SET new_rank=? WHERE id=?',
            (prev_ranks[node], node)
            )
cur.execute('UPDATE Pages SET old_rank = new_rank')
conn.commit()
