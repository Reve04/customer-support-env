import difflib

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


def get_ideal_response(ticket):
    dept = ticket["department"]
    if dept == "billing":
        return "We sincerely apologize for the billing issue. We will review your account, correct any errors immediately, and process a full refund if necessary."
    elif dept == "technical":
        return "We are looking into the technical issue you reported. Our engineering team has been notified and is currently investigating the error to deploy a fix as soon as possible."
    else:
        return "Thank you for reaching out to us. We appreciate your feedback and have passed your message along to the relevant team for review."


def grade_task3(action, ticket):
    priority_score, priority_feedback = grade_task2(action, ticket)
    base_score = priority_score * 0.6

    draft = action.draft_response or ""
    draft_score = 0.0
    feedback = priority_feedback

    if len(draft) < 20:
        feedback += " Draft too short."
    else:
        ideal_response = get_ideal_response(ticket)
        # Calculate Python's native text structural similarity
        # Returns a float [0, 1] characterizing the similarity
        sim = difflib.SequenceMatcher(None, draft.lower(), ideal_response.lower()).ratio()
        
        # Scale similarity to a max of 0.4
        # Since difflib.ratio rarely hits 1.0 unless perfectly identical,
        # anything above 0.5 is actually extremely good phrasing overlap.
        scaled_sim = max(0.0, min(1.0, (sim - 0.1) / 0.6)) 
        draft_score = round(scaled_sim * 0.4, 2)
        feedback += f" Semantic match score: {round(scaled_sim*100)}%."

    total = round(base_score + draft_score, 2)
    return total, feedback