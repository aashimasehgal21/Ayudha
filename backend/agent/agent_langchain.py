# backend/agent/agent_langchain.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.agent.agent_core import _llm_answer

try:
    from backend.rag.test_rag import run_rag_pipeline
except Exception:
    run_rag_pipeline = None

try:
    from backend.nlp.sentiment import analyze_sentiment
except Exception:
    analyze_sentiment = None

try:
    from backend.security.prompt_guard import guard, get_safe_response
except Exception:
    guard = None
    get_safe_response = None

try:
    from backend.nlp.lang_support import process_with_lang
except Exception:
    process_with_lang = None


# --------------------------------------------------
# REASONER
# --------------------------------------------------
class AyudhaAgentReasoner:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        self.prompt = ChatPromptTemplate.from_template("""
You are a routing assistant for a legal AI system for women's safety in India.

Decide if the user query needs legal retrieval (RAG)
or a direct conversational response (DIRECT).

Choose RAG if the user asks about:
- IPC sections
- Laws or legal acts
- FIR procedures
- Legal rights
- Complaint templates
- Harassment, stalking, dowry, domestic violence
- POSH, POCSO, cybercrime

Choose DIRECT for:
- Greetings
- Casual chat
- Emotional support
- General questions
- Simple conversations

User query: {query}

Reply with ONLY one word:
RAG or DIRECT
""")

        self.chain = self.prompt | self.llm | StrOutputParser()

    def decide(self, user_query: str) -> str:
        try:
            result = self.chain.invoke({"query": user_query})

            cleaned = result.strip().upper()

            if "RAG" in cleaned:
                return "RAG"

            return "DIRECT"

        except Exception as e:
            print(f"[Reasoner Error] {e}")
            return "DIRECT"


# --------------------------------------------------
# EXECUTOR
# --------------------------------------------------
class AyudhaAgentExecutor:

    def __init__(self):
        self.reasoner = AyudhaAgentReasoner()

    def answer(self, user_query: str) -> str:

        # --------------------------------------------------
        # 1. SECURITY CHECK
        # --------------------------------------------------
        if guard:

            safe_query, threat = guard(user_query)

            if threat == "INJECTION_DETECTED":
                return get_safe_response(threat)

            if threat == "EMPTY_INPUT":
                return "Please ask your question — I am here to help you."

            user_query = safe_query

        # --------------------------------------------------
        # 2. SENTIMENT ANALYSIS
        # --------------------------------------------------
        sentiment = {}

        if analyze_sentiment:
            try:
                sentiment = analyze_sentiment(user_query)
                print(f"[Sentiment] {sentiment}")

            except Exception as e:
                print(f"[Sentiment Error] {e}")

        # --------------------------------------------------
        # 3. EMERGENCY OVERRIDE
        # --------------------------------------------------
        if sentiment.get("is_emergency"):

            result = (
                "I hear you. Please stay safe and contact help immediately.\n\n"
                "🆘 Emergency: 112\n"
                "👩 Women Helpline: 1091\n"
                "🏠 Domestic Violence: 181\n\n"
                "Are you currently safe?"
            )

            if process_with_lang:
                result = process_with_lang(user_query, result)

            return result

        # --------------------------------------------------
        # 4. EMPATHY PREFIX
        # --------------------------------------------------
        prefix = ""

        if sentiment.get("needs_empathy"):

            prefix = (
                "I understand this may be difficult for you. "
                "You are not alone.\n\n"
            )

        # --------------------------------------------------
        # 5. ROUTING DECISION
        # --------------------------------------------------
        decision = self.reasoner.decide(user_query)

        print(f"[Agent] Decision: {decision}")

        # --------------------------------------------------
        # 6. RAG FLOW
        # --------------------------------------------------
        if decision == "RAG" and run_rag_pipeline:

            try:

                rag_answer = run_rag_pipeline(user_query)

                # Remove source text if present
                if isinstance(rag_answer, str) and "SOURCE:" in rag_answer:
                    rag_answer = rag_answer.split("SOURCE:")[0].strip()

                # --------------------------------------------------
                # SUMMARIZATION LAYER
                # --------------------------------------------------
                summary_prompt = f"""
You are Ayudha, a women's legal assistant.

Convert this legal answer into a:
- short
- conversational
- user-friendly response

Rules:
- 10 lines
- Use simple language
- First explain the law 
- Then give practical guidance
- Keep the original legal meaning accurate
- Avoid unnecessary legal theory
- Mention IPC/law only if necessary
- Do not change the actual law or IPC section meaning
- End by asking if the user wants more details

Legal answer:
{rag_answer}
"""

                rag_answer = _llm_answer(summary_prompt)

                result = prefix + rag_answer

                if process_with_lang:
                    result = process_with_lang(user_query, result)

                return result

            except Exception as e:

                print(f"[RAG Error] {e}")

                result = prefix + _llm_answer(user_query)

                if process_with_lang:
                    result = process_with_lang(user_query, result)

                return result

        # --------------------------------------------------
        # 7. DIRECT LLM RESPONSE
        # --------------------------------------------------
        result = prefix + _llm_answer(user_query)

        if process_with_lang:
            result = process_with_lang(user_query, result)

        return result