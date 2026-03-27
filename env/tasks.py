TICKETS = [
    {
        "ticket_id": "T001",
        "subject": "Can't log into my account",
        "body": "I have been trying to log in for 2 hours. It keeps saying wrong password but I just reset it. Please help urgently.",
        "customer_tier": "pro",
        "account_age_days": 180,
        "priority": "high",
        "department": "technical",
        "keywords": ["password", "reset", "login", "access"]
    },
    {
        "ticket_id": "T002",
        "subject": "Question about pricing",
        "body": "Hi, I was just wondering if you offer any student discounts. No rush, just curious before I upgrade.",
        "customer_tier": "free",
        "account_age_days": 14,
        "priority": "low",
        "department": "billing",
        "keywords": ["discount", "pricing", "plan", "upgrade"]
    },
    {
        "ticket_id": "T003",
        "subject": "Wrong charge on my invoice",
        "body": "I was charged twice this month. I need this fixed immediately and a refund issued. This is unacceptable.",
        "customer_tier": "enterprise",
        "account_age_days": 730,
        "priority": "high",
        "department": "billing",
        "keywords": ["refund", "invoice", "charge", "account review"]
    },
    {
        "ticket_id": "T004",
        "subject": "How do I export my data?",
        "body": "I would like to know how to export all my project data to CSV. Is that possible?",
        "customer_tier": "pro",
        "account_age_days": 90,
        "priority": "medium",
        "department": "technical",
        "keywords": ["export", "csv", "data", "download"]
    },
    {
        "ticket_id": "T005",
        "subject": "App is very slow today",
        "body": "Everything is loading extremely slowly since this morning. My whole team is affected and we have a deadline today.",
        "customer_tier": "enterprise",
        "account_age_days": 400,
        "priority": "high",
        "department": "technical",
        "keywords": ["slow", "performance", "loading", "team"]
    },
    {
        "ticket_id": "T006",
        "subject": "Cancel my subscription",
        "body": "Please cancel my subscription at the end of this billing cycle. I no longer need the service.",
        "customer_tier": "pro",
        "account_age_days": 365,
        "priority": "medium",
        "department": "billing",
        "keywords": ["cancel", "subscription", "billing cycle", "refund"]
    },
    {
        "ticket_id": "T007",
        "subject": "Feature request: dark mode",
        "body": "It would be great if you could add a dark mode to the app. Many users have been asking for this.",
        "customer_tier": "free",
        "account_age_days": 60,
        "priority": "low",
        "department": "general",
        "keywords": ["feature", "dark mode", "request", "suggestion"]
    },
    {
        "ticket_id": "T008",
        "subject": "API integration not working",
        "body": "Our developer has been trying to connect your API for 3 days. We are getting 401 errors on every call. This is blocking our entire product launch.",
        "customer_tier": "enterprise",
        "account_age_days": 200,
        "priority": "high",
        "department": "technical",
        "keywords": ["api", "401", "authentication", "integration", "error"]
    },
    {
        "ticket_id": "T009",
        "subject": "Feedback on onboarding",
        "body": "Just wanted to say the onboarding experience was really smooth. One small suggestion: maybe add a video tutorial?",
        "customer_tier": "free",
        "account_age_days": 7,
        "priority": "low",
        "department": "general",
        "keywords": ["feedback", "onboarding", "tutorial", "suggestion"]
    },
    {
        "ticket_id": "T010",
        "subject": "Data not syncing between devices",
        "body": "My data is not syncing between my phone and laptop. I have tried reinstalling the app but the problem persists.",
        "customer_tier": "pro",
        "account_age_days": 120,
        "priority": "medium",
        "department": "technical",
        "keywords": ["sync", "devices", "data", "reinstall"]
    }
]

TASKS = {
    "task1": {
        "name": "task1",
        "description": "Classify the priority of the ticket: low, medium, or high.",
        "difficulty": "easy",
        "action_schema": {
            "priority": "one of: low, medium, high"
        }
    },
    "task2": {
        "name": "task2",
        "description": "Classify priority AND route to the correct department: billing, technical, or general.",
        "difficulty": "medium",
        "action_schema": {
            "priority": "one of: low, medium, high",
            "department": "one of: billing, technical, general"
        }
    },
    "task3": {
        "name": "task3",
        "description": "Classify priority, route to department, AND write a helpful draft response to the customer.",
        "difficulty": "hard",
        "action_schema": {
            "priority": "one of: low, medium, high",
            "department": "one of: billing, technical, general",
            "draft_response": "a short helpful reply to the customer"
        }
    }
}