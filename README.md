# PageRank Web Crawler & Visualization

This project is a **Python-based simulation of a search engine ranking system** inspired by Google’s original **PageRank algorithm**.

It crawls web pages, stores link relationships in a database, computes PageRank scores using an iterative algorithm, and visualizes the web structure as an interactive graph.

This is an **educational project** focused on understanding how search engines work internally.

---

## 📌 What This Project Does

1. Crawls web pages starting from a seed URL  
2. Extracts and stores links between pages  
3. Builds a directed graph of the website  
4. Computes PageRank scores iteratively  
5. Visualizes the web graph using a force-directed layout  

---

## 🛠️ Technologies Used

- **Python**
- **SQLite** (database storage)
- **BeautifulSoup** (HTML parsing)
- **urllib** (HTTP requests)
- **D3.js** (graph visualization)
- **HTML / JavaScript**

---

## 📂 Project Structure

pagerank-web-crawler/
│
├── spider.py        # Crawls web pages and stores links
├── sprank.py        # Computes PageRank values
├── spdump.py        # Quick inspection of link counts
├── spjson.py        # Converts data to graph format
├── force.html       # Graph visualization (D3.js)
├── spider.js        # Generated graph data
├── .gitignore
└── README.md

---

## ▶️ How to Run the Project

### 1️⃣ Install dependency
```bash
pip install beautifulsoup4


⸻

2️⃣ Run the web crawler

python spider.py

	•	Enter a starting URL when prompted
	•	Crawling is intentionally limited to a single domain

⸻

3️⃣ Compute PageRank

python sprank.py

	•	Enter number of iterations (e.g., 10)

⸻

4️⃣ Generate visualization data

python spjson.py

	•	Enter number of nodes to visualize (e.g., 20)

⸻

5️⃣ View the graph

python -m http.server 8000

Open in browser:

http://localhost:8000/force.html


⸻

📊 Visualization
	•	Node size represents PageRank importance
	•	Links represent page connections
	•	Nodes are draggable for interaction

⸻

📘 What I Learned
	•	How web crawlers collect and structure data
	•	How PageRank distributes importance across links
	•	How iterative algorithms converge
	•	How graph theory applies to real-world systems
	•	How backend data can be visualized interactively

⸻

⚠️ Notes
	•	Crawling is ethical and domain-restricted
	•	Visualization performance depends on node count
	•	This is not a production search engine
	•	Built for learning and experimentation

⸻

🙏 Acknowledgment

Inspired by the Python for Everybody course by
Dr. Charles R. Severance (Coursera)

⸻

👤 Author

Gurlal Singh
Computer Science Student
Python | Data Structures | Algorithms

⸻

⭐ If you find this project useful, feel free to star the repository.
