#  Webiste content Searcher SPA

A **Single Page Application** (SPA) that allows users to input a website URL and a search query. It fetches the HTML content from the provided site, tokenizes and chunks it, and returns the top 10 relevant content snippets using semantic search.

---

##  Features

###  Frontend (Next.js)
- Two input fields:
  - **Website URL**
  - **Search Query**
- Used tailwindCSS for styling and shadcn for components
- Submit button to trigger search
- Displays top 10 matching chunks (max 500 tokens each) in card/table layout

###  Backend (Python - Flask)
- Fetch HTML content
- Tokenize and chunk content
- Perform semantic search using vector database (Weaviate)
- Return top 10 most relevant HTML chunks

---

##  Tech Stack

| Layer     | Technology                |
|-----------|---------------------------|
| Frontend  | Next.js        |
| Backend   | Python (Flask)  |
| HTML Parsing | BeautifulSoup          |
| Tokenization | Transformers (MiniLM)    |
| Vector DB | Weaviate |

---

##  Setup Instructions

### Prerequisites
- Node.js (v20+)
- Python (3.12+)
- pip
- Vector DB setup ( Weaviate - cloud)

---

### 🛠️ Frontend Setup

```bash
cd client
npm install
npm run dev
```
---
### Backend Setup

```bash
cd backend
pip install bs4 requests weaviate weaviate-client dotenv flask flask_cors urllib
python app.py
```
## Vector DB Configuration
1. Set up your vector DB Weaviate cloud on sandbox for free trial of 15 days and create a cluster.

2. Get you credentials like WEAVIATE_CLUSTER_URL and WEAVIATE_API_KEY and configure those in .env

3. Ensure the backend connects successfully before running queries.

root/<br/>
│<br/>
├── cient/              # React or Next.js frontend<br/>
│   └── app/           # Application directory<br/>
│&emsp;&emsp;&emsp;└── page.tsx/ #SPA form for searching<br/>
│<br/>
├── backend/               # Python backend<br/>
│   └── app.py             # Main API server, <br/>
│   └── search.py          # HTML parsing logic, Vector DB integration, Tokenization & chunking <br/>
│<br/>
└── README.md<br/>
