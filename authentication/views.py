from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def home(req):
    print("from home")
    return render(req,"authentication/index.html")

def successLogin(req):
    return render(req,"authentication/success.html")

# create account
def signup(req):
    if req.method == "POST":
        userName = req.POST.get("userName")
        pass1 = req.POST.get("pass1")
        print("done")
        myuser = User.objects.create_user(username=userName,password=pass1)
        myuser.save()
        messages.success(req,"Successfully Created")
        return redirect('signin') 
    return render(req,"authentication/signup.html")


#Login
def signin(req):
   
    if req.method == "POST":
        userName = req.POST.get("userName")
        pass1 = req.POST.get("pass1")
        user1 = authenticate(username = userName , password=pass1 )
        

        if user1 is not None:
            
            login(req,user1)
            return render(req,"authentication/success.html")
        else:
           
            messages.error(req,"Bad Credential")
            return redirect("signin")
        
    return render(req,"authentication/signin.html")
    

# logout

def signout(req):
    logout(req)
    messages.success("Successfully Logout")
    return redirect('home')

   