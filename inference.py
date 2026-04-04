import os
import json
import urllib.request
import re
from openai import OpenAI

# Define the local environment URL, OpenEnv generally maps to 7860 dynamically via Docker
ENV_URL = os.environ.get("ENV_URL", "http://127.0.0.1:7860")

# Retrieve Mandatory Environment Variables
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.environ.get("OPENAI_API_KEY", os.environ.get("HF_TOKEN", "your-token"))

# Initialize OpenAI Client (per mandatory requirements)
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def env_call(method, path, data=None, params=None):
    url = ENV_URL + path
    if params:
        url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
    body = json.dumps(data).encode() if data else None
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def extract_json_from_response(content):
    """Fallback logic to safely parse JSON from the LLM."""
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    # Baseline fallback if parsing totally fails
    return {"priority": "medium", "department": "general", "draft_response": "Thank you for your message."}


def get_llm_action(obs, task_name):
    prompt = f"""
You are an AI customer support triage agent. 
Based on the ticket details, classify the priority, department, and draft a response if requested.
Ticket Subject: {obs.get('subject')}
Ticket Body: {obs.get('body')}

Based on the ticket, determine the following:
"""
    req_keys = []
    if task_name == "task1":
        prompt += "- priority: MUST be one of 'low', 'medium', 'high'\n"
        req_keys = ["priority"]
    elif task_name == "task2":
        prompt += "- priority: MUST be one of 'low', 'medium', 'high'\n"
        prompt += "- department: MUST be one of 'billing', 'technical', 'general'\n"
        req_keys = ["priority", "department"]
    else:  # task3
        prompt += "- priority: MUST be one of 'low', 'medium', 'high'\n"
        prompt += "- department: MUST be one of 'billing', 'technical', 'general'\n"
        prompt += "- draft_response: a brief and helpful reply string for the customer\n"
        req_keys = ["priority", "department", "draft_response"]

    prompt += "\nOutput your response strictly as JSON in the following format:\n"
    prompt += "{\n" + ",\n".join(f'  "{k}": "..."' for k in req_keys) + "\n}"

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content
        action = extract_json_from_response(content)
        
        # Pruning the action to only include exactly what the task requires
        filtered_action = {k: action.get(k, "general") for k in req_keys}
        # Edge case default fixing
        if 'priority' in filtered_action and filtered_action['priority'] not in ['low', 'medium', 'high']:
            filtered_action['priority'] = 'medium'
            
        return filtered_action
    except Exception as e:
        print(f"Error calling LLM: {e}")
        # Return naive fallback immediately
        return {"priority": "medium", "department": "general", "draft_response": "Thank you."}


def run_inference():
    print("Starting LLM evaluations...", flush=True)
    all_tasks = ["task1", "task2", "task3"]

    for task_name in all_tasks:
        print(f"[START] {task_name}", flush=True)
        # Running 5 episodes per task, similar to the legacy baseline
        for i in range(5):
            obs = env_call("POST", "/reset", params={"task_name": task_name})
            done = False
            while not done:
                action = get_llm_action(obs, task_name)
                print(f"[STEP] Task: {task_name} | Episode: {i+1} | Action Taken: {json.dumps(action)}", flush=True)
                
                result = env_call("POST", f"/step?task_name={task_name}", data=action)
                done = result["done"]
                obs = result.get("observation", {})
                
        print(f"[END] {task_name}", flush=True)


if __name__ == "__main__":
    run_inference()
