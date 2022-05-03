from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .utilities import run_statement
from django.shortcuts import redirect

# Create your views here.

def index(req):
    return render(req,'siteIndex.html')

def instructor(req):
    
    isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
    
    return render(req,'siteIndex.html')



def logout(req):
    req.session.flush()
    return HttpResponseRedirect('/dbmanagement') #Redirect user to home page
