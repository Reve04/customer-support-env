def grade_task1(action, ticket):
    correct = ticket["priority"]
    guess = action.priority.lower().strip()

    if guess == correct:
        return 1.0, "Correct priority."

    priority_order = ["low", "medium", "high"]
    if correct in priority_order and guess in priority_order:
        diff = abs(priority_order.index(guess) - priority_order.index(correct))
        if diff == 1:
            return 0.5, f"Off by one. Expected {correct}, got {guess}."

    return 0.0, f"Wrong priority. Expected {correct}, got {guess}."


def grade_task2(action, ticket):
    score = 0.0
    feedback_parts = []

    correct_priority = ticket["priority"]
    guess_priority = action.priority.lower().strip()

    if guess_priority == correct_priority:
        score += 0.5
        feedback_parts.append("Priority correct.")
    else:
        priority_order = ["low", "medium", "high"]
        if correct_priority in priority_order and guess_priority in priority_order:
            diff = abs(priority_order.index(guess_priority) - priority_order.index(correct_priority))
            if diff == 1:
                score += 0.25
                feedback_parts.append(f"Priority off by one. Expected {correct_priority}, got {guess_priority}.")
            else:
                feedback_parts.append(f"Priority wrong. Expected {correct_priority}, got {guess_priority}.")
        else:
            feedback_parts.append(f"Priority wrong. Expected {correct_priority}, got {guess_priority}.")

    correct_dept = ticket["department"]
    guess_dept = action.department.lower().strip() if action.department else ""

    if guess_dept == correct_dept:
        score += 0.5
        feedback_parts.append("Department correct.")
    else:
        feedback_parts.append(f"Department wrong. Expected {correct_dept}, got {guess_dept}.")

    return round(score, 2), " ".join(feedback_parts)


def grade_task3(action, ticket):
    priority_score, priority_feedback = grade_task2(action, ticket)
    base_score = priority_score * 0.6

    draft = action.draft_response or ""
    draft_lower = draft.lower()
    keywords = ticket["keywords"]

    matched = [kw for kw in keywords if kw.lower() in draft_lower]
    keyword_ratio = len(matched) / len(keywords) if keywords else 0
    draft_score = round(keyword_ratio * 0.4, 2)

    total = round(base_score + draft_score, 2)

    feedback = priority_feedback
    feedback += f" Draft matched {len(matched)}/{len(keywords)} expected keywords."
    if len(draft) < 20:
        feedback += " Draft too short."
        total = max(0.0, total - 0.1)

    return total, feedback