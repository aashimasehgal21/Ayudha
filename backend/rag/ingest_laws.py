import os
from dotenv import load_dotenv
from openai import OpenAI
from backend.db.supabase_client import get_supabase_client

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #Secure API initialization using environment variables.

def embed(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def load_laws():
    supabase = get_supabase_client()
    folder = "backend/data/laws"

    for filename in os.listdir(folder): #every file -law 
        if filename.endswith(".txt"): # process text file 
            title = filename.replace(".txt", "")
            full_path = os.path.join(folder, filename)

            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            embedding = embed(content)

            supabase.table("laws").insert({
                "title": title,
                "content": content,
                "embedding": embedding
            }).execute()

            print(f"Inserted law → {title}")


if __name__ == "__main__":
    load_laws()


#ingests legal text files, generates semantic embeddings using OpenAI, and stores both the raw text and 
#vectors in Supabase, enabling efficient similarity-based retrieval in a RAG system