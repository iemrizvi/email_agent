import json
from agents.classifier import classify_email
from agents.drafter import draft_reply
from agents.logger import log_result

with open("data/mock_emails.json") as f:
    emails = json.load(f)

print("Starting email agent...\n")

for email in emails:
    print(f"Processing: {email['subject']}")

    label = classify_email(email["subject"], email["body"])
    print(f"  Label: {label}")

    if label == "spam":
        draft = "[No reply — marked as spam]"
        log_result(email, label, draft)
        print()
        continue

    draft = draft_reply(email, label)
    flagged = label == "complaint"

    print(f"  Draft: {draft[:80]}...")
    if flagged:
        print(f"  Flagged as complaint!")

    log_result(email, label, draft, flagged=flagged)
    print()

print("Done! Check MongoDB Compass to see your results.")