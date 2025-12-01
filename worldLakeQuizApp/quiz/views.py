from django.shortcuts import render
import random
from lakes.models import Lake


# Create your views here.
def quiz_lakes(request):
    question = Lake.objects.order_by('?').first()

    if request.method == "POST":
        user_answer = request.POST.get("answer")
        correct_answer = request.session.get("country")
        is_correct = (user_answer == correct_answer)
        context = {
            "is_correct": is_correct,
            "correct_answer": correct_answer
        }
        return render(request, "quiz/result.html", context)

    wrong_answers = (
        Lake.objects.exclude(country=question.country)
        .order_by('?')
        .values_list('country', flat=True)[:3]
    )
    options = list(wrong_answers)
    options.append(question.country)
    
    random.shuffle(options)

    request.session["country"] = question.country

    context = {
        'question': question,
        'options': options
    }

    return render(request, 'quiz/quiz_lakes.html', context)
