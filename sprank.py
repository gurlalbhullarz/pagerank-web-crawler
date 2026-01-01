"""
sprank.py
---------
Computes PageRank values for crawled pages
using an iterative graph-based algorithm.
"""

import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('SELECT DISTINCT from_id FROM Links')
from_ids = [row[0] for row in cur]

if not from_ids:
    print('No links found')
    quit()

links = []
cur.execute('SELECT DISTINCT from_id, to_id FROM Links')
for from_id, to_id in cur:
    if from_id == to_id:
        continue
    if from_id not in from_ids or to_id not in from_ids:
        continue
    links.append((from_id, to_id))

prev_ranks = {}
cur.execute('SELECT id, old_rank FROM Pages')
for id, rank in cur:
    prev_ranks[id] = rank

iterations = input('How many iterations: ')
iterations = int(iterations) if iterations.isdigit() else 1

for i in range(iterations):
    print(f'Iteration {i + 1}')

    next_ranks = {node: 0.0 for node in prev_ranks}
    total = sum(prev_ranks.values())

    for node, old_rank in prev_ranks.items():
        targets = [to_id for from_id, to_id in links if from_id == node]
        if not targets:
            continue

        share = old_rank / len(targets)
        for target in targets:
            next_ranks[target] += share

    evap = (total - sum(next_ranks.values())) / len(next_ranks)
    for node in next_ranks:
        next_ranks[node] += evap

    diff = sum(abs(prev_ranks[n] - next_ranks[n]) for n in prev_ranks)
    print('Average change:', diff / len(prev_ranks))

    prev_ranks = next_ranks

for node, rank in prev_ranks.items():
    cur.execute('UPDATE Pages SET new_rank=? WHERE id=?', (rank, node))

cur.execute('UPDATE Pages SET old_rank=new_rank')
conn.commit()
print('PageRank computation complete')
