from django.shortcuts import render
from django.http import HttpResponse

def index(response):
    HttpResponse('hello world')

# Create your views here.
