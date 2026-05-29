# backend/memory/test_memory_chat.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from backend.memory.conversation_memory import get_session_history


def run_test():
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    chain = prompt | llm

    chain_with_memory = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    session_id = "test-session"

    print(chain_with_memory.invoke(
        {"input": "My name is Aashima"},
        config={"configurable": {"session_id": session_id}}
    ))

    print(chain_with_memory.invoke(
        {"input": "What is my name?"},
        config={"configurable": {"session_id": session_id}}
    ))


if __name__ == "__main__":
    run_test()
