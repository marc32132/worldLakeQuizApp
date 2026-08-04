from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import random
from lakes.models import Lake
from .models import QuizResult

# Number of quiz questions per session
QUESTIONS_NUM = 5

# Number of quiz options per question
OPTIONS_NUM = 4

# Number of results displayed per page for authenticated user
PAGE_SIZE = 10


def quiz_lakes(request):
    """
    Handles the quiz flow:
    - GET: generates random lake questions with multiple-choice answers
    - POST: evaluates submitted answers, stores results in session and saves them to database for authenticated users
    """

    # Handle quiz submission
    if request.method == "POST":
        user_answers = request.POST
        correct_answers = request.session.get("correct_answers", {})

        # Calculate score
        results, score = calculate_score(correct_answers, user_answers)
        total = len(correct_answers)

        # Save results to database
        if request.user.is_authenticated:
            quiz_result = QuizResult.objects.create(
                user = request.user,
                score = score,
                total = total
            )
            for r in results:
                quiz_result.answers.create(
                    question=r["question"],
                    user_answer=r["user_answer"],
                    correct_answer=r["correct_answer"],
                    is_correct=r["is_correct"]
                )

        # Save results in session for display
        request.session["quiz_results"] = {
            "results": [{
                        "question": r["question"].name,
                        "user_answer": r["user_answer"],
                        "correct_answer": r["correct_answer"],
                        "is_correct": r["is_correct"]
                        } for r in results],
            "score": score,
            "total": total
        }

        # Remove answers to prevent resubmission issues
        request.session.pop("correct_answers", None)
        
        return redirect("quiz:quiz_results")

    # Generate random questions
    quiz_data, correct_answers = generate_questions()

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


@login_required
def saved_results(request):
    results = QuizResult.objects.filter(
        user=request.user
    ).order_by("-created_at")
    
    p = Paginator(results, PAGE_SIZE)
    page = p.get_page(request.GET.get("page"))

    context = {
        "results": results,
        "paginated_results": page
    }
    if request.headers.get("HX-Request"):
        return render(request, "quiz/partials/results_history.html", context)

    return render(request, "quiz/saved_results.html", context)

@login_required
def result_detail(request, result_id):
    result = get_object_or_404(
        QuizResult,
        id=result_id,
        user=request.user
    )


    return render(request, "quiz/result_detail.html", {
        "result": result
    })

def generate_questions():
    # Generate random questions
    questions = list(Lake.objects.order_by('?')[:QUESTIONS_NUM])
    quiz_data = []
    correct_answers = {}

    for question in questions:

        # Get unique countries excluding the correct one
        other_countries = list(
            Lake.objects
            .exclude(country=question.country)
            .values_list('country', flat=True)
            .order_by('country')
            .distinct()
        )

        wrong_answers = random.sample(other_countries, OPTIONS_NUM - 1)

        options = wrong_answers + [question.country]       
        random.shuffle(options)

        quiz_data.append({
            "id": question.id,
            "name": question.name,
            "options": options,
        })

        # Store correct answer in session (key must be string for POST data matching)
        correct_answers[str(question.id)] = question.country

    return quiz_data, correct_answers


def calculate_score(correct_answers, user_answers):
    score = 0
    results = []

    lakes = Lake.objects.in_bulk(correct_answers.keys())

    # Compare user answers with correct ones stored in session
    for q_id, correct_country in correct_answers.items():
        user_answer = user_answers.get(q_id)
        is_correct = user_answer == correct_country

        if is_correct:
            score += 1
        
        lake = lakes[int(q_id)]

        # Store detailed result for each question
        results.append({
            "question": lake,
            "user_answer": user_answer,
            "correct_answer": correct_country,
            "is_correct": is_correct
            })
        
    return results, score