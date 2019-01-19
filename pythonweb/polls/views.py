from django.shortcuts import render, reverse, get_object_or_404
from .models import Question, Choice
from django.http import HttpResponseRedirect


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
    error = None
    if request.method == 'POST':
        if request.POST.get('choice'):
            movie = Choice.objects.get(id=request.POST.get('choice'))
            movie.votes += 1
            movie.save()
            return HttpResponseRedirect(reverse('polls:result', args=(
                question_id,
            )))
        else:
            error = 'Please choice an option'

    question, answers = get_answer_question(question_id)
    content = {
        'question': question,
        'answers': answers,
        'error': error
    }
    return render(request, 'polls/detail.html', content)


def result(request, question_id):
    question, answers = get_answer_question(question_id)
    total_votes = sum([movie.votes for movie in answers])
    content = {
        'result': answers,
        'question': question,
        'total_votes': total_votes
    }
    return render(request, 'polls/result.html', content)
