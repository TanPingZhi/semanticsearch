from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import pandas as pd
import time

# Initialize Elasticsearch client
es = Elasticsearch(["http://localhost:9200"])

# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Index name
index_name = "philosopher_quotes"

df = pd.read_csv("hf://datasets/datastax/philosopher-quotes/philosopher-quotes.csv")
df = df.drop(columns=["tags"])
df.reset_index(inplace=True)
df.rename(columns={'index': 'id'}, inplace=True)

documents = df.to_dict(orient="records")

def create_index():
    # Create index with dense vector field
    index_settings = {
        "mappings": {
            "properties": {
                "author": {"type": "text"},
                "quote": {"type": "text"},
                "content_vector": {"type": "dense_vector", "dims": 384}
            }
        }
    }
    es.indices.create(index=index_name, body=index_settings, ignore=400)
    print(f"Index '{index_name}' created or already exists.")



def index_documents():
    duration = 0
    for doc in documents:
        # Encode the quote
        start_time = time.time()  # Record start time
        vector = model.encode(doc["quote"])
        end_time = time.time()  # Record end time
        duration += end_time - start_time
        # Prepare the document
        document = {
            "author": doc["author"],
            "quote": doc["quote"],
            "content_vector": vector.tolist()
        }

        # Index the document
        es.index(index=index_name, id=doc["id"], body=document)

    print("Encoded all documents in {:.2f} seconds.".format(duration))


def main():
    print("Creating index...")
    create_index()

    print("Indexing documents...")
    index_documents()

    print("Finished indexing documents.")


if __name__ == "__main__":
    main()