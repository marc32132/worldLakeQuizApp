from django.shortcuts import render, redirect
import random
from lakes.models import Lake

# Number of quiz questionst per session
QUESTIONS_NUM = 5

# Number of quiz options per question
OPTIONS_NUM = 4


def quiz_lakes(request):
    """
    Handles the quiz flow:
    - GET: generates random lake questions with multiple-choice answers
    - POST: evaluates submitted answers and stores results in session
    """

    # Handle quiz submission
    if request.method == "POST":
        user_answers = request.POST
        correct_answers = request.session.get("correct_answers", {})

        score = 0
        results = []

        # Compare user answers with correct ones stored in session
        for q_id, correct_country in correct_answers.items():
            user_answer = user_answers.get(q_id)
            is_correct = user_answer == correct_country

            if is_correct:
                score += 1

            # Store detailed result for each question
            results.append({
                "question_id": q_id,
                "question_name": Lake.objects.get(id=q_id).name,
                "user_answer": user_answer,
                "correct_answer": correct_country,
                "is_correct": is_correct,
            })

        # Save results in session for the results view
        request.session["quiz_results"] = {
            "results": results,
            "score": score,
            "total": len(correct_answers)
        }

        # Remove answers to prevent resubmission issues
        request.session.pop("correct_answers", None)
        
        return redirect("quiz:quiz_results")

    # Generate random questions (database-level random ordering)
    questions = list(Lake.objects.order_by('?')[:QUESTIONS_NUM])
    quiz_data = []
    correct_answers = {}

    for question in questions:

        # Get unique countries excluding the correct one
        other_countries = list(
            Lake.objects
            .exclude(country=question.country)
            .values_list('country', flat=True)
            .distinct()
        )

        # Randomly pick incorrect options
        wrong_answers = random.sample(other_countries, OPTIONS_NUM - 1)

        # Combine correct and incorrect answers and shuffle
        options = wrong_answers + [question.country]       
        random.shuffle(options)

        # Prepare data for template rendering
        quiz_data.append({
            "id": question.id,
            "name": question.name,
            "options": options,
        })

        # Store correct answer in session (key must be string for POST data matching)
        correct_answers[str(question.id)] = question.country

    # Save correct answers for later validation
    request.session["correct_answers"] = correct_answers

    return render(request, 'quiz/quiz_lakes.html', {"quiz_data": quiz_data})


def quiz_results(request):
    """
    Displays quiz results stored in session.
    Redirects to quiz start if no results are available.
    """

    quiz_data = request.session.get("quiz_results")

    # Prevent direct access without completing quiz
    if not quiz_data:
        return redirect("quiz:quiz_lakes")
    
    # Clear results after displaying (one-time view)
    request.session.pop("quiz_results", None)

    return render(request, "quiz/result.html", quiz_data)