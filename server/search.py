from bs4 import BeautifulSoup
import requests
import weaviate
from weaviate.classes.query import MetadataQuery
from sentence_transformers import SentenceTransformer
from weaviate.exceptions import WeaviateBaseError
import time
from dotenv import load_dotenv
import os 
load_dotenv()
API_KEY = os.getenv("WEAVIATE_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_CLUSTER_URL")



# --- Initialize embedding model ---
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_all_endpoints(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('/'):
            links.add(base_url.rstrip('/') + href)
        elif href.startswith(base_url):
            links.add(href)
    return list(links) + [base_url]

def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "meta", "link"]):
        tag.decompose()
    return soup

def chunk_text(text, max_tokens=500):
    words = text.split()
    return [' '.join(words[i:i+max_tokens]) for i in range(0, len(words), max_tokens)]

def index_website(url, client,collection_name="WebsiteChunks"):
    html = requests.get(url).text
    soup = clean_html(html)
    text = soup.get_text(separator=' ', strip=True)
    chunks = chunk_text(text, max_tokens=500)

    try:
        client.collections.get(collection_name)
        collection_exists = True
    except Exception:
        collection_exists = False

    if not collection_exists:
        client.collections.create(
            name=collection_name,
            vectorizer_config=weaviate.classes.config.Configure.Vectorizer.none(),
            properties=[
                weaviate.classes.config.Property(name="content", data_type=weaviate.classes.config.DataType.TEXT),
                weaviate.classes.config.Property(name="url", data_type=weaviate.classes.config.DataType.TEXT)
            ]
        )
    collection = client.collections.get(collection_name)

    # 3. Index chunks with embeddings
    with collection.batch.dynamic() as batch:
        for chunk in chunks:
            embedding = model.encode(chunk).tolist()
            batch.add_object(
                properties={"content": chunk, "url": url,"html":str(soup)},
                vector=embedding
            )
    print(f"Indexed {len(chunks)} chunks from {url}")


def semantic_search(query,model,base_url, client,collection_name="WebsiteChunks", top_k=50):
    collection = client.collections.get(collection_name)
    query_embedding = model.encode(query).tolist()
    results = collection.query.near_vector(
        near_vector=query_embedding,
        limit=top_k,
        return_metadata=MetadataQuery(distance=True)
    )
    answers = []
    for obj in results.objects:
        if obj.properties['url'].startswith(base_url):
            result = {
                "score": round(1-obj.metadata.distance,3),
                "url" : obj.properties['url'],
                "content" : obj.properties['content'][:300]
            }
            if obj.properties.get('html'):
                result["html"] = obj.properties['html'][2324:4000]
            if result not in answers:
                answers.append(result)
    return answers


def search(website_url, user_query,model=model):
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_URL,
        auth_credentials=weaviate.auth.AuthApiKey(API_KEY)
    )

    start = time.perf_counter()
    endpoints = get_all_endpoints(website_url)
    for endpoint in endpoints:
        index_website(endpoint,client)
    answer = semantic_search(user_query,model,website_url,client)
    
    end = time.perf_counter()
    client.close()
    return answer,end-start
    