---
title: Customer Support Triage Env
emoji: 🎫
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
tags:
  - openenv
---

# Customer Support Triage Environment

An OpenEnv-compatible reinforcement learning environment where an AI agent
learns to handle real-world customer support tickets.

## What the agent does
The agent reads a customer support ticket and must:
- Classify the urgency (low / medium / high)
- Route it to the right department (billing / technical / general)
- Draft a helpful reply to the customer

## Tasks

| Task | Difficulty | Description |
|------|------------|-------------|
| task1 | Easy | Classify priority only |
| task2 | Medium | Classify priority + route to department |
| task3 | Hard | Priority + routing + draft response |

## Observation Space
- `ticket_id` - unique ticket identifier
- `subject` - ticket subject line
- `body` - full ticket message
- `customer_tier` - free / pro / enterprise
- `account_age_days` - how long the customer has been active
- `task_name` - which task the agent is solving

## Action Space
- `priority` - one of: low, medium, high
- `department` - one of: billing, technical, general
- `draft_response` - a helpful reply string (task3 only)

## Reward
- Range: 0.0 to 1.0
- Partial credit awarded for off-by-one priority errors
- Task3 rewards keyword coverage in the draft response

## Baseline Scores
- task1: 1.0
- task2: 1.0
- task3: 0.78

## Setup
```bash
pip install -r requirements.txt
python -m uvicorn api.main:app --reload
```

## Docker
```bash
docker build -t customer-support-env .
docker run -p 7860:7860 customer-support-env
```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /reset | POST | Start a new episode |
| /step | POST | Submit an action |
| /state | GET | Get current state |
| /tasks | GET | List all tasks |
| /grader | GET | Get grader info |
| /baseline | GET | Run baseline agent |