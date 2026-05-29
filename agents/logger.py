from db.mongo import emails_col
from datetime import datetime

def log_result(email: dict, label: str, draft: str, flagged: bool = False):
    doc = {
        "email_id": email["id"],
        "from": email["from"],
        "subject": email["subject"],
        "label": label,
        "draft_reply": draft,
        "flagged": flagged,
        "processed_at": datetime.utcnow()
    }
    emails_col.insert_one(doc)
    print(f"  Saved to MongoDB")