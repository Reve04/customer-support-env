import json
import random

# Read the existing file
with open("env/tasks.py", "r") as f:
    original_code = f.read()

# Define the data templates for procedural generation
technical_templates = [
    ("Cannot login to dashboard", "It says invalid credentials but I am sure they are correct.", "high", ["login", "credentials", "dashboard"]),
    ("API rate limit error", "Hitting the limit even on enterprise tier.", "high", ["api", "limit", "rate"]),
    ("App crashes on iOS", "Force closing immediately after the new update.", "high", ["app", "crash", "ios", "update"]),
    ("Export to CSV failing", "I get a 500 error when I try to export my report.", "medium", ["export", "csv", "error", "500"]),
    ("Data not syncing", "Desktop client won't sync with mobile app.", "medium", ["sync", "desktop", "mobile"]),
    ("Webhook delivery failed", "Missing notifications since yesterday.", "high", ["webhook", "delivery", "notification"]),
    ("Slow query performance", "Database queries are timing out.", "medium", ["slow", "query", "performance", "timeout"]),
    ("2FA setup not sending SMS", "I am not receiving the text message to set up 2FA.", "medium", ["2fa", "sms", "text", "auth"]),
    ("Profile picture won't upload", "Keeps saying format invalid for standard jpeg.", "low", ["upload", "picture", "format"]),
    ("Integration with Slack broken", "The slack bot stopped responding to commands.", "medium", ["slack", "integration", "bot"])
]

billing_templates = [
    ("Refund request", "I forgot to cancel, please refund this month.", "medium", ["refund", "cancel", "month"]),
    ("Double charge on card", "I see two identical charges on my statement.", "high", ["charge", "double", "statement"]),
    ("Update payment method", "Where do I go to change my credit card?", "low", ["payment", "card", "update"]),
    ("Invoice missing VAT", "My company needs an invoice with our VAT number.", "medium", ["invoice", "vat", "tax"]),
    ("Downgrade my account", "I want to move from Pro to Free layer.", "medium", ["downgrade", "pro", "free"]),
    ("Coupon code not working", "Applied the promo code but it still charged full price.", "medium", ["coupon", "promo", "price"]),
    ("Unrecognized charge", "What is this $50 charge from your company?", "high", ["unrecognized", "charge", "fraud"]),
    ("Change billing cycle", "Can we switch from monthly to annual billing?", "low", ["billing", "cycle", "annual"]),
    ("Receipt for accounting", "Need a copy of all receipts for last year.", "low", ["receipt", "accounting", "year"]),
    ("Student discount application", "Here is my university ID, can I get the discount?", "low", ["student", "discount", "id"])
]

general_templates = [
    ("How do I add a team member?", "Looking for the user management screen.", "low", ["team", "member", "management"]),
    ("Delete my account", "I no longer wish to use the service, please delete everything.", "medium", ["delete", "account", "remove"]),
    ("Feature request: dark theme", "My eyes hurt, please add a dark mode.", "low", ["feature", "dark", "theme"]),
    ("Enterprise sales inquiry", "We have 10,000 employees and want a demo.", "medium", ["enterprise", "sales", "demo"]),
    ("Is there a mobile app?", "Do you have an Android version available?", "low", ["mobile", "app", "android"]),
    ("Spam from your platform", "Someone is sending me spam messages through your app.", "high", ["spam", "abuse", "report"]),
    ("Feedback on new UI", "The new layout is very confusing.", "low", ["feedback", "ui", "layout"]),
    ("Partnership opportunity", "We would love to integrate our tools.", "low", ["partnership", "integrate", "opportunity"]),
    ("GDPR data request", "I would like a copy of all my data under GDPR.", "medium", ["gdpr", "data", "request"]),
    ("Where are the docs?", "I can't find the documentation for the webhooks.", "low", ["docs", "documentation", "webhooks"])
]

all_templates = []
for template_group, dept in [(technical_templates, "technical"), (billing_templates, "billing"), (general_templates, "general")]:
    for t in template_group:
        all_templates.append((t[0], t[1], dept, t[2], t[3]))

# Generate 40 tickets randomly
tiers = ["free", "pro", "enterprise"]
new_tickets = []
for i in range(11, 51):
    template = random.choice(all_templates)
    ticket = {
        "ticket_id": f"T{str(i).zfill(3)}",
        "subject": template[0],
        "body": template[1],
        "customer_tier": random.choice(tiers),
        "account_age_days": random.randint(1, 1000),
        "priority": template[3],
        "department": template[2],
        "keywords": template[4]
    }
    new_tickets.append(ticket)

# Now, we parse the TICKETS list in env/tasks.py and append them.
# The easiest way is to inject the new items into the text where TICKETS ends.
# We find the string "]\n\nTASKS =" and replace it.

new_dicts_str = ",\n".join([json.dumps(nt, indent=4) for nt in new_tickets])
# We have to indent it nicely
new_dicts_str = "    " + new_dicts_str.replace("\n", "\n    ")

if "]\n\nTASKS =" in original_code:
    new_code = original_code.replace("]\n\nTASKS =", ",\n" + new_dicts_str + "\n]\n\nTASKS =")
    with open("env/tasks.py", "w") as f:
        f.write(new_code)
    print("Successfully appended 40 new tickets to env/tasks.py")
else:
    print("Could not find insertion marker in env/tasks.py")
