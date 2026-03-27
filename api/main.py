from fastapi import FastAPI
from env.models import Action
from env.environment import CustomerSupportEnv
from env.tasks import TASKS

app = FastAPI()

envs = {
    "task1": CustomerSupportEnv(task_name="task1"),
    "task2": CustomerSupportEnv(task_name="task2"),
    "task3": CustomerSupportEnv(task_name="task3"),
}

@app.post("/reset")
def reset(task_name: str = "task1"):
    env = envs.get(task_name)
    if not env:
        return {"error": "Unknown task name."}
    obs = env.reset()
    return obs.model_dump()

@app.post("/step")
def step(action: Action, task_name: str = "task1"):
    env = envs.get(task_name)
    if not env:
        return {"error": "Unknown task name."}
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.model_dump(),
        "reward": reward.model_dump(),
        "done": done,
        "info": info
    }

@app.get("/state")
def state(task_name: str = "task1"):
    env = envs.get(task_name)
    if not env:
        return {"error": "Unknown task name."}
    return env.state()

@app.get("/tasks")
def tasks():
    return TASKS

@app.get("/grader")
def grader(task_name: str = "task1"):
    env = envs.get(task_name)
    if not env:
        return {"error": "Unknown task name."}
    return {
        "task_name": task_name,
        "last_state": env.state()
    }

@app.get("/baseline")
def baseline():
    results = {}
    for task_name, env in envs.items():
        scores = []
        for _ in range(10):
            env.reset()
            if task_name == "task1":
                action = Action(priority="high")
            elif task_name == "task2":
                action = Action(priority="high", department="technical")
            else:
                action = Action(
                    priority="high",
                    department="technical",
                    draft_response="Thank you for contacting us. We will review your account and resolve this issue as soon as possible."
                )
            _, reward, _, _ = env.step(action)
            scores.append(reward.score)
        results[task_name] = round(sum(scores) / len(scores), 2)
    return results