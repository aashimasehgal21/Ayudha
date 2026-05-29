import os
from dotenv import load_dotenv
from openai import OpenAI
from backend.db.supabase_client import get_supabase_client

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def load_procedures():
    supabase = get_supabase_client()
    folder = "backend/data/procedures"

    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            title = filename.replace(".txt", "")
            full_path = os.path.join(folder, filename)

            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            embedding = embed(content)

            supabase.table("procedures").insert({
                "title": title,
                "content": content,
                "embedding": embedding
            }).execute()

            print(f"Inserted procedure → {title}")


if __name__ == "__main__":
    load_procedures()
