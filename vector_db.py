from dotenv import load_dotenv
load_dotenv()
import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance,VectorParams

def setup_qdrant_database():
    try:
        client=QdrantClient(path="./qdrant_storage")
        collection_name="pdf_search"
        if not client.collection_exists(collection_name):
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
            
            print(f"Collection : {collection_name} is ready")
        
        else:
            print(f"Collection {collection_name} already exists in our Vector Database ")

        return client,collection_name
    #Raising Error if collection not found
    except Exception as e:
        print(f"Error : {e}")
        return None,None

