import random
from env.models import Observation, Action, Reward
from env.tasks import TICKETS, TASKS
from env.graders import grade_task1, grade_task2, grade_task3

class CustomerSupportEnv:
    def __init__(self, task_name="task1"):
        self.task_name = task_name
        self.current_ticket = None
        self.done = False
        self.step_count = 0
        self.max_steps = 10

    def reset(self):
        self.current_ticket = random.choice(TICKETS)
        self.done = False
        self.step_count = 0
        return self._make_observation()

    def step(self, action: Action):
        if self.done:
            obs = self._make_observation()
            reward = Reward(score=0.0, max_score=1.0, feedback="Episode already done. Call reset.")
            return obs, reward, self.done, {}

        self.step_count += 1

        score, feedback = self._grade(action)
        reward = Reward(score=score, max_score=1.0, feedback=feedback)

        self.done = True
        self.current_ticket = random.choice(TICKETS)

        return self._make_observation(), reward, self.done, {}

    def state(self):
        return {
            "task_name": self.task_name,
            "step_count": self.step_count,
            "done": self.done,
            "current_ticket_id": self.current_ticket["ticket_id"] if self.current_ticket else None
        }

    def _make_observation(self):
        t = self.current_ticket
        return Observation(
            ticket_id=t["ticket_id"],
            subject=t["subject"],
            body=t["body"],
            customer_tier=t["customer_tier"],
            account_age_days=t["account_age_days"],
            task_name=self.task_name
        )

    def _grade(self, action: Action):
        if self.task_name == "task1":
            return grade_task1(action, self.current_ticket)
        elif self.task_name == "task2":
            return grade_task2(action, self.current_ticket)
        elif self.task_name == "task3":
            return grade_task3(action, self.current_ticket)
        else:
            return 0.0, "Unknown task."