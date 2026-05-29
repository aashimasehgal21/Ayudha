# backend/rag/test_rag.py

from openai import OpenAI
from backend.rag.rag_search import retrieve
from backend.rag.rag_prompt_builder import create_rag_prompt

client = OpenAI()   # Reads API key automatically from .env


def run_rag_pipeline(query: str) -> str:
    """
    Main RAG pipeline:
    1. Retrieve relevant context from Supabase
    2. Create the combined text prompt
    3. Call OpenAI ChatCompletion API correctly
    4. Return clean final answer
    """
    try: #error if any
        print("[Agent] 🧠 Running RAG Pipeline...")

        
        # Retrieve context from Supabase
        
        context = retrieve(query, total_k=6)

        
        #Build final combined prompt 
       
        prompt = create_rag_prompt(query, context)

        
        # Call ChatCompletion 
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a legal assistant. Use ONLY the provided context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

       
        # Extract answer correctly 
        
        final_answer = response.choices[0].message.content
        print("\n[Agent] ✅ FINAL RAG ANSWER:\n", final_answer)

        return final_answer

    except Exception as e:
        import traceback
        print("❌ RAG PIPELINE ERROR:", e)
        traceback.print_exc()
        return f"ERROR: {str(e)}"
