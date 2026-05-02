import os
import pickle
import numpy as np
import faiss 
import time
import torch 
from sentence_transformers import SentenceTransformer 

DATA_PATH = "knowledge.txt"
DB_PATH = "db"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

MODEL_NAME = "paraphrase-MiniLM-L3-v2"  

BATCH_SIZE = 16        
SLEEP_TIME = 0.7       

MAX_CHUNKS = 10000     
torch.set_num_threads(1)  


# LOAD TEXT
def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# CHUNKING
def chunk_text(text, chunk_size, overlap):
    chunks = []
    start = 0

    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap

    return chunks


# LOAD MODEL
def load_model():
    print("Loading model...")
    model = SentenceTransformer(MODEL_NAME)
    print("Model loaded!")
    return model


# BUILD INDEX (SAFE MODE)
def build_or_load_index(model, chunks):
    index_path = os.path.join(DB_PATH, "index.faiss")

    # Step 1: Load existing index if exists
    if os.path.exists(index_path):
        print("Loading existing FAISS index...")
        index = faiss.read_index(index_path)
    else:
        print("Creating new FAISS index...")
        sample = model.encode(["test"])
        dim = len(sample[0])
        index = faiss.IndexFlatL2(dim)

    total = len(chunks)

    print("Adding new embeddings...")

    for i in range(0, total, BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]

        embeddings = model.encode(batch, show_progress_bar=False)
        embeddings = np.array(embeddings).astype("float32")

        index.add(embeddings)

        print(f"⚡ Added: {i + len(batch)} / {total}")

        time.sleep(SLEEP_TIME)

    print("Index updated!")
    return index

# SAVE
def save_db(index, new_chunks):
    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)

    index_path = os.path.join(DB_PATH, "index.faiss")
    chunk_path = os.path.join(DB_PATH, "chunks.pkl")

    # Save index
    faiss.write_index(index, index_path)

    # Append chunks
    if os.path.exists(chunk_path):
        with open(chunk_path, "rb") as f:
            old_chunks = pickle.load(f)
        all_chunks = old_chunks + new_chunks
    else:
        all_chunks = new_chunks

    with open(chunk_path, "wb") as f:
        pickle.dump(all_chunks, f)

    print(f"Total chunks stored: {len(all_chunks)}")

# MAIN
def main():
    print("Starting SAFE ingestion...\n")

    text = load_text(DATA_PATH)
    chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

    print(f"Total chunks: {len(chunks)}")

    #LIMIT WORKLOAD
    # chunks = chunks[:MAX_CHUNKS]
    chunks = chunks[30000:]
    print(f"⚡ Processing only: {len(chunks)} chunks (safe mode)")

    model = load_model()

    index = build_or_load_index(model, chunks)

    save_db(index, chunks)
    print(index.ntotal)
    print(len(chunks))
    print("\nSAFE ingestion complete!")


# RUN
if __name__ == "__main__":
    main()