import os
import sys

from env.graders import grade_task1, grade_task2, grade_task3
from env.tasks import TICKETS
from env.models import Action

for i, ticket in enumerate(TICKETS):
    a1 = Action(priority=ticket["priority"])
    score1, _ = grade_task1(a1, ticket)
    if not (0 < score1 < 1): print(f"Task1 Ticket {i} exact bound! score={score1}")

    a2 = Action(priority=ticket["priority"], department=ticket["department"])
    score2, _ = grade_task2(a2, ticket)
    if not (0 < score2 < 1): print(f"Task2 Ticket {i} exact bound! score={score2}")

    a3 = Action(priority=ticket["priority"], department=ticket["department"], draft_response="TEST DRAFT STRING OF LENGTH GREATER THAN 20 WHICH IS LONG")
    score3, _ = grade_task3(a3, ticket)
    if not (0 < score3 < 1): print(f"Task3 Ticket {i} exact bound! score={score3}")

print("Done scanning grader bounds.")
