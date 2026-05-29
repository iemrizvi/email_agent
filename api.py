from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from db.mongo import emails_col
from agents.classifier import classify_email
from agents.drafter import draft_reply
from agents.logger import log_result
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class Email(BaseModel):
    id: str
    sender: str
    subject: str
    body: str

@app.get("/", response_class=HTMLResponse)
def index():
    with open("templates/index.html") as f:
        return f.read()

@app.post("/process")
def process_email(email: Email):
    email_dict = {
        "id": email.id,
        "from": email.sender,
        "subject": email.subject,
        "body": email.body
    }
    label = classify_email(email.subject, email.body)
    
    if label == "spam":
        draft = "[No reply — marked as spam]"
        flagged = False
    else:
        draft = draft_reply(email_dict, label)
        flagged = label == "complaint"
    
    log_result(email_dict, label, draft, flagged)
    
    return {
        "id": email.id,
        "label": label,
        "draft": draft,
        "flagged": flagged
    }

@app.get("/emails")
def get_emails():
    emails = list(emails_col.find({}, {"_id": 0}).sort("processed_at", -1))
    return emails