from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

prompt = ChatPromptTemplate.from_template("""
You are a professional customer support agent.
The incoming email is classified as: {label}

Write a concise, professional reply to this email.
Keep it under 5 sentences.

From: {sender}
Subject: {subject}
Body: {body}

Reply:
""")

chain = prompt | llm

def draft_reply(email: dict, label: str) -> str:
    result = chain.invoke({
        "label": label,
        "sender": email["from"],
        "subject": email["subject"],
        "body": email["body"]
    })
    return result.content.strip()