from django.shortcuts import render
from django.http import HttpResponse
import pandas
# Create your views here.
def home(request):
    return render(request, 'transform/home.html')
def upload(request):
    print("Testing")