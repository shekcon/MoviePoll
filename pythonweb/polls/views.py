from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Choice


# Create your views here.
def index(request, *args, **kwargs):
    
    content = {
        'questions': Question.objects.all()
    }
    return render(request, 'polls/index.html', content)


def get_answer_question(_id):
    question = get_object_or_404(Question, id=_id)
    answers = question.answer.all()
    return question, answers


def detail(request, question_id):
    
    if request.method == 'POST' and request.POST.get('choice'):
        print(request.POST)
        movie = Choice.objects.get(id=request.POST.get('choice'))
        movie.votes += 1
        movie.save()
        return redirect('result', question_id=question_id)

    question, answers = get_answer_question(question_id)
    content = {
        'question': question,
        'answers': answers
    }
    return render(request, 'polls/detail.html', content)
    

def result(request, question_id):
    question, answers = get_answer_question(question_id)
    content = {
        'result': answers,
        'question': question
    }
    return render(request, 'polls/result.html', content)