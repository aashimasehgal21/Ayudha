# backend/agent/test_agent_langchain.py

from backend.agent.agent_langchain import AyudhaAgentExecutor


def run_tests():
    agent = AyudhaAgentExecutor()

    test_queries = [
        # RAG-type queries
        "What is IPC Section 498A?",
        "How to file an FIR in India?",
        "Give me a sample legal notice format",

        # DIRECT-type queries
        "What is the difference between law and ethics?",
        "Explain legal rights in simple words",
        "Hello, how are you?"
    ]

    for q in test_queries:
        print("\n==============================")
        print(f"USER QUERY: {q}")
        answer = agent.answer(q)
        print("AGENT ANSWER:")
        print(answer)


if __name__ == "__main__":
    run_tests()
