import pandas as pd 
from sqlalchemy import text
import logging
from Services.ingestservice import getengine
from sentence_transformers import SentenceTransformer
import logging
import os 
import faiss
import numpy as np
logger = logging.getLogger(__name__)

def getreviewsforembedding():
    try:
        df= pd.read_sql("select * from bronze.reviews" ,getengine())
        logger.info(f"Sales data fetched {len(df)}")
        df = df[["review_id","product_title","review_headline","review_body"] ]
        df = df.dropna(subset=["review_body"])
        df = df[df["review_body"].str.strip() != ""]
        df = df.drop_duplicates(subset=["review_id"])
        logger.info(f"After cleaning: {len(df)} rows")
        return df
    except Exception as e:
        logger.error(f"getreviewsforembedding failed: {e}")
        return None
    

def generateembeddings(df):
    logger.info(f"Generating embeddings for {len(df)} reviews")
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    review = df["review_body"].tolist()
    encode = model.encode(review)
    logger.info(f"Embeddings generated: shape {encode.shape}")
    return df, encode


VECTOR_STORE_DIR = "./vectorstore"
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

def build_faiss_index(df, vectors):
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors).astype('float32'))
    index_path = os.path.join(VECTOR_STORE_DIR, "review_index.faiss")
    mapping_path = os.path.join(VECTOR_STORE_DIR, "review_mapping.csv")
    faiss.write_index(index, index_path)
    df.reset_index(drop=True).to_csv(mapping_path, index=True)
    logger.info(f"FAISS index built and saved: {index.ntotal} vectors")
    return index


def searchreviews(query, top_k=5):
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
     
    index = faiss.read_index("./vectorstore/review_index.faiss")
    mapping = pd.read_csv("./vectorstore/review_mapping.csv")
     
    query_vector = model.encode([query]).astype('float32')
     
    distances, indices = index.search(query_vector, top_k)
     
    results = mapping.iloc[indices[0]]
    
    return results