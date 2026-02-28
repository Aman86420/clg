def calculate_score(answers: list[int], correct_answers: list[int]) -> float:
    if len(answers) != len(correct_answers):
        raise ValueError("Answer count mismatch")
    
    correct = sum(1 for user_ans, correct_ans in zip(answers, correct_answers) if user_ans == correct_ans)
    return (correct / len(correct_answers)) * 100
