import os
import faiss # type: ignore
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer # type: ignore
from google import genai




# CONFIG
DB_PATH = "../db"
MODEL_NAME = "paraphrase-MiniLM-L3-v2"
TOP_K = 5


client = genai.Client(api_key="AIzaSyDQB2juxQPosYYECSIU4jdxqLXkcBoC4XQ")

# LOAD DB
def load_db():
    index_path = os.path.join(DB_PATH, "index.faiss")
    chunk_path = os.path.join(DB_PATH, "chunks.pkl")

    if not os.path.exists(index_path) or not os.path.exists(chunk_path):
        raise Exception("❌ DB not found. Run ingest.py first.")

    print("📂 Loading FAISS index...")
    index = faiss.read_index(index_path)

    print("📂 Loading chunks...")
    with open(chunk_path, "rb") as f:
        chunks = pickle.load(f)

    print(f"✅ Loaded {len(chunks)} chunks")
    return index, chunks


# LOAD MODEL
def load_model():
    print("🔄 Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)
    print("✅ Model ready!")
    return model


# SEARCH
def search(query, model, index, chunks):
    query_vec = model.encode([query]).astype("float32")

    D, I = index.search(query_vec, TOP_K)

    results = [chunks[i] for i in I[0]]
    return results


# GEMINI RESPONSE
def generate_answer(query, context):
    context_text = "\n".join(context)

    prompt = f"""
Answer the question using ONLY the context below.

Context:
{context_text}

Question:
{query}

Answer:
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# MAIN LOOP
def main():
    print("Gemini RAG System Started...\n")

    index, chunks = load_db()
    model = load_model()

    while True:
        query = input("\nAsk your question (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        # Step 1: Retrieve
        results = search(query, model, index, chunks)

        print("\nRetrieved Context:\n")
        for i, r in enumerate(results):
            print(f"{i+1}. {r[:200]}...\n")

        # Step 2: Generate Answer
        answer = generate_answer(query, results)

        print("\nAnswer:\n")
        print(answer)


if __name__ == "__main__":
    main()