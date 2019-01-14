from django.shortcuts import render
from django.http import HttpResponse
from .models import Question


# Create your views here.
def index(request, *args, **kwargs):
    
    content = {
        'questions': Question.objects.all()
    }
    return render(request, 'polls/index.html', content)

def detail(request, question_id):
    content = {
        'question': Question.objects.get(id=question_id)
    }
    return render(request, 'polls/detail.html', content)
    
def result(request, *args, **kwargs):
    content = {
        
    }
    return render(request, 'polls/result.html', content)