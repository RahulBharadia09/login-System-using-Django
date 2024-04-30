from django.http import HttpResponse;
from django.shortcuts import redirect, render;
from django.contrib.auth.models import User;
from django.contrib import messages;
from django.contrib.auth import authenticate,login,logout;
from authhhh import settings;
from django.core.mail import send_mail,EmailMessage ;
from django.contrib.sites.shortcuts import get_current_site;
from django.template.loader import render_to_string;
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode;
from django.utils.encoding import force_bytes,force_str;
from .token import generate_token;
from django.contrib.auth.views import PasswordResetView;


# Create your views here.


def home(req):
    print("from home")
    return render(req,"authentication/index.html")

def successLogin(req):
    return render(req,"authentication/success.html")

# create account
def signup(req):
    if req.method == "POST":
        username = req.POST.get("userName")
        pass1 = req.POST.get("pass1")
        email = req.POST.get("email")
        fname = req.POST.get("fname")
        lname = req.POST.get("lname")
        
        if User.objects.filter(username=username):
            messages.error(req,"Username already exists please try another username")
            return redirect('signin')
        
        # if User.objects.filter(email=email):
        #    messages.error(req,"Username already exists please try another username")
        #    return redirect('signin')
        
        if len(username)>12:
           messages.error(req,"Username character must be less then 12")
           return redirect('signin')
    
        # if pass1 != pass2:
        #    messages.error(req,'Confirm password doesnt match with the password')
        #    messages.error(req,"Username already exists please try another username")
        #    return redirect('signin')

        if not username.isalnum():
            messages.error(req,"Username must be alphanumeric")
            return redirect('signin')
           



        myuser = User.objects.create_user(username=username,password=pass1,email=email,first_name=fname,last_name = lname)
        myuser.is_active= False
        myuser.save()
        messages.success(req,"Successfully Created")


        # welcome message:

        subject = "Welcome to MyPortfolio" + myuser.first_name + "login Credential"
        message = "Hello" + myuser.first_name + "\n Thank you for the enquiry \n we have sent you the mail for verification \n Please verify your account in order to actiavte your account \n\n Thank You \n Rahul Bharadia"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email,]
        send_mail(subject,message,from_email,to_list,fail_silently=True)
        # email confirmation email
        current_site = get_current_site(req)
        email_subject = "confirm your email @ - Rahul Bharadia"
        message2 = render_to_string('email_confirmation.html',{
            'name':myuser.first_name,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser)
        })
        email= EmailMessage (
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email]

        )
        email.fail_silently =True
        email.send()

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
            first_name=user1.first_name
            messages.success(req,"Successfull")
            return render(req,"authentication/success.html",{'first_name':first_name})
        else:
           
            messages.error(req,"Bad Credential")
            return redirect("signin")
        
    return render(req,"authentication/signin.html")
    

# logout

def signout(req):
    logout(req)
    messages.success("Successfully Logout")
    return redirect('home')

# confirmation logic 
def activate(req,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError, User.DoesNotExits):
        myuser=None
    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active=True
        myuser.save()
        login(req,myuser)
        return redirect('success')
    else:
        return render(req,'activation_failed.html')

# Password Reset function
def PasswordReset(req):
   pass
    