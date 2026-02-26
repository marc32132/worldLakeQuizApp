from django.shortcuts import render, redirect
import random
from lakes.models import Lake

QUESTIONS_NUM = 5
OPTIONS_NUM = 4

# Create your views here.
def quiz_lakes(request):

    if request.method == "POST":
        user_answers = request.POST
        correct_answers = request.session.get("correct_answers", {})

        score = 0
        results = []

        for q_id, correct_country in correct_answers.items():
            user_answer = user_answers.get(q_id)
            is_correct = user_answer == correct_country

            if is_correct:
                score += 1

            results.append({
                "question_id": q_id,
                "question_name": Lake.objects.get(id=q_id).name,
                "user_answer": user_answer,
                "correct_answer": correct_country,
                "is_correct": is_correct,
            })


        request.session["quiz_results"] = {
            "results": results,
            "score": score,
            "total": len(correct_answers)
        }
        request.session.pop("correct_answers", None)
        return redirect("quiz:quiz_results")

    questions = list(Lake.objects.order_by('?')[:QUESTIONS_NUM])
    quiz_data = []
    correct_answers = {}

    for question in questions:

        other_countries = list(
            Lake.objects
            .exclude(country=question.country)
            .values_list('country', flat=True)
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
        correct_answers[str(question.id)] = question.country

    request.session["correct_answers"] = correct_answers


    return render(request, 'quiz/quiz_lakes.html', {"quiz_data": quiz_data})


def quiz_results(request):
    quiz_data = request.session.get("quiz_results")

    if not quiz_data:
        return redirect("quiz:quiz_lakes")
    
    request.session.pop("quiz_results", None)

    return render(request, "quiz/result.html", quiz_data)