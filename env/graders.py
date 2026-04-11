def _clamp(score):
    """Enforce strict open interval (0, 1). Also handles NaN/inf safely."""
    try:
        v = float(score)
        # NaN check: NaN != NaN is always True
        if v != v or v == float('inf') or v == float('-inf'):
            return 0.5
        return max(0.01, min(0.99, v))
    except (ValueError, TypeError):
        return 0.5


def grade_task1(action, ticket):
    correct = ticket["priority"]
    guess = action.priority.lower().strip()

    if guess == correct:
        return _clamp(0.99), "Correct priority."

    priority_order = ["low", "medium", "high"]
    if correct in priority_order and guess in priority_order:
        diff = abs(priority_order.index(guess) - priority_order.index(correct))
        if diff == 1:
            return _clamp(0.5), f"Off by one. Expected {correct}, got {guess}."

    return _clamp(0.01), f"Wrong priority. Expected {correct}, got {guess}."


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

    return _clamp(round(score, 2)), " ".join(feedback_parts)


def get_ideal_response(ticket):
    dept = ticket["department"]
    if dept == "billing":
        return "We sincerely apologize for the billing issue. We will review your account, correct any errors immediately, and process a full refund if necessary."
    elif dept == "technical":
        return "We are looking into the technical issue you reported. Our engineering team has been notified and is currently investigating the error to deploy a fix as soon as possible."
    else:
        return "Thank you for reaching out to us. We appreciate your feedback and have passed your message along to the relevant team for review."


def grade_task3(action, ticket):
    """
    Grades task3: priority + department (60%) + draft response quality (40%).
    Uses keyword-based scoring for the draft response - fast, deterministic, no model needed.
    """
    priority_score, priority_feedback = grade_task2(action, ticket)
    base_score = priority_score * 0.6

    draft = action.draft_response or ""
    draft_lower = draft.lower()
    feedback = priority_feedback

    if len(draft) < 20:
        feedback += " Draft too short."
        draft_score = 0.0
    else:
        # Keyword coverage scoring using ticket's own keyword list
        keywords = ticket.get("keywords", [])
        if keywords:
            matches = sum(1 for kw in keywords if kw.lower() in draft_lower)
            keyword_ratio = matches / len(keywords)
        else:
            keyword_ratio = 0.5  # neutral if no keywords defined

        # Also check for department-appropriate language
        ideal = get_ideal_response(ticket).lower()
        ideal_words = set(ideal.split())
        draft_words = set(draft_lower.split())
        overlap = len(ideal_words & draft_words)
        word_ratio = min(1.0, overlap / max(len(ideal_words), 1))

        # Blend keyword coverage and word overlap
        combined = (keyword_ratio * 0.6) + (word_ratio * 0.4)
        draft_score = round(combined * 0.4, 3)
        feedback += f" Draft quality: {int(combined * 100)}%."

    total = round(base_score + draft_score, 3)
    return _clamp(total), feedback