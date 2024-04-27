from django.shortcuts import render
from django.http import  HttpResponse

# Create your views here.
def home(req):
    return render(req,"authentication/index.html")

def signin(req):
    return render(req,"authentication/signin.html")
    

def signup(req):
    return render(req,"authentication/signup.html")
