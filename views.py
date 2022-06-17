from django.contrib import messages
from django.shortcuts import render

# Create your views here.
import requests
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse

from .models import *
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .emailbackend import emailbackend

def loginpage(request):
    return render(request, "client_app/login.html")

def dologin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method not Allowed</h2>")
    else:

        user=emailbackend.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!= None:
             login(request,user)
             if user.user_type=="1":
              #return render(request, "student_management_app/index.html")
                  return HttpResponseRedirect(reverse("admin_home"))
             else:
              #return render(request, "student_management_app/index.html")
                  return HttpResponseRedirect(reverse("client_home"))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")


def user_details(request):
    if request.user != None:
      return HttpResponse("User : "+request.user.email+ "Usertype : "+str(request.user.user_type ))
    else:
      return HttpResponse("Please login first")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

