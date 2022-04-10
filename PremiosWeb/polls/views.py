

from unittest import expectedFailure
from urllib import response
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Choise, Question

# Create your views here.

def index(request):
    questions = Question.objects.all()
    context = {
        'questions': questions,
    }
    return render(request, 'polls/index.html', context) 


def detail(request, response_id):
    question = get_object_or_404(Question,pk=response_id)
    context = {
        'question': question,
    }
    return render(request, 'polls/detail.html', context) 


def result(request, response_id):
    question = get_object_or_404(Question, pk=response_id)
    return render(request, 'polls/result.html', {
        "question": question,
        'response_id': response_id,
    })

def vote(request, response_id):
    question = get_object_or_404(Question, pk=response_id)
    try:
        find_choise = question.choise_set.get(pk=request.POST['choise'])
    except (KeyError, Choise.DoesNotExist):
        return render(request,'polls/detail.html', {
            'question': question,
            'error_message': "no elegiste ninguna respuesta"
        })
    else:
        find_choise.votes += 1
        find_choise.save()
        return HttpResponseRedirect(reverse("polls:result", args=(response_id)))


# def vote(request, response_id):
#     question = get_object_or_404(Question, pk=response_id)
#     try:
#         selected_choise = question.choise_set.get(pk=request.POST['choise'])
#     except (KeyError,Choise.DoesNotExist):
#         return render(request,'polls/detail.html', {
#             "question": question,
#             "error_message": "no elegiste ningun valor",
#         })
#     else:
#         selected_choise.votes += 1
#         selected_choise.save()
#         return HttpResponseRedirect(reverse("polls:result", args=(response_id,)))