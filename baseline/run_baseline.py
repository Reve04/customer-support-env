import urllib.request
import urllib.error
import json

BASE_URL = "http://127.0.0.1:8000"

def call(method, path, data=None, params=None):
    url = BASE_URL + path
    if params:
        url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
    body = json.dumps(data).encode() if data else None
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def simple_agent(observation, task_name):
    body = observation.get("body", "").lower()
    subject = observation.get("subject", "").lower()
    text = body + " " + subject

    urgent_words = ["urgent", "immediately", "blocked", "can't", "error", "wrong charge", "slow", "not working", "launch"]
    low_words = ["question", "wondering", "curious", "feedback", "suggestion", "feature request"]

    if any(w in text for w in urgent_words):
        priority = "high"
    elif any(w in text for w in low_words):
        priority = "low"
    else:
        priority = "medium"

    billing_words = ["charge", "invoice", "refund", "billing", "pricing", "subscription", "discount", "cancel"]
    technical_words = ["login", "api", "error", "sync", "export", "slow", "loading", "password", "integration"]

    if any(w in text for w in billing_words):
        department = "billing"
    elif any(w in text for w in technical_words):
        department = "technical"
    else:
        department = "general"

    draft = (
        f"Thank you for reaching out to us. We have received your request regarding '{observation.get('subject', '')}'. "
        f"Our {department} team will review your account and resolve this issue as soon as possible. "
        f"We apologize for any inconvenience caused and appreciate your patience."
    )

    if task_name == "task1":
        return {"priority": priority}
    elif task_name == "task2":
        return {"priority": priority, "department": department}
    else:
        return {"priority": priority, "department": department, "draft_response": draft}

def run_baseline():
    print("Running baseline agent...\n")
    all_results = {}

    for task_name in ["task1", "task2", "task3"]:
        scores = []
        for i in range(10):
            obs = call("POST", "/reset", params={"task_name": task_name})
            action = simple_agent(obs, task_name)
            result = call("POST", f"/step?task_name={task_name}", data=action)
            score = result["reward"]["score"]
            scores.append(score)

        avg = round(sum(scores) / len(scores), 2)
        all_results[task_name] = avg
        print(f"{task_name}: average score = {avg}")

    print("\nBaseline complete.")
    print(json.dumps(all_results, indent=2))
    return all_results

if __name__ == "__main__":
    run_baseline()