from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

prompt = ChatPromptTemplate.from_template("""
You are an email classifier. Classify this email into exactly one of these labels:
inquiry, complaint, spam, other

Email subject: {subject}
Email body: {body}

Respond with ONLY the label word, nothing else. Lowercase only.
""")

chain = prompt | llm

def classify_email(subject: str, body: str) -> str:
    result = chain.invoke({"subject": subject, "body": body})
    return result.content.strip().lower()