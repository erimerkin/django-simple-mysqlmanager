from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .db_utils import run_statement
from django.shortcuts import redirect

# Create your views here.

def index(req):
    #Logout the user if logged 
    if req.session:
        if "type" in req.session:
            user_type = req.session["type"]
            if (user_type == 0):
                return redirect('../instructor/')
            elif (user_type == 1):
                return redirect('../student/')
            else:
                return redirect('../manager/')

    
    isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
    return render(req,'siteIndex.html')

def loginIndex(req):
    #Logout the user if logged 
    if req.session:
        req.session.flush()
    
    isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
    
    loginForm=UserLoginForm() #Use Django Form object to create a blank form for the HTML page

    return render(req,'siteIndex.html')

def instructor(req):
    
    isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
    
    return render(req,'siteIndex.html')

def instructor_login(req):
    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"SELECT * FROM User WHERE username='{username}' and password='{password}';") #Run the query in DB

    if result: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        req.session["type"]=0
        return HttpResponseRedirect('../userHome') #Redirect user to home page
    else:
        return HttpResponseRedirect('../loginIndex?fail=true')

def student_login(req):
    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"SELECT * FROM User WHERE username='{username}' and password='{password}';") #Run the query in DB

    if result: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        req.session["type"]= 1
        return HttpResponseRedirect('../userHome') #Redirect user to home page
    else:
        return HttpResponseRedirect('../loginIndex?fail=true')

def manager_login(req):
    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"SELECT * FROM DBManager WHERE username='{username}' and password='{password}';") #Run the query in DB

    if result: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        req.session["type"]=2
        return HttpResponseRedirect('../userHome') #Redirect user to home page
    else:
        return HttpResponseRedirect('../loginIndex?fail=true')


def login(req, user_type):
    
    
    result=run_statement(f"SELECT * FROM {user_type} WHERE username='{username}' and password='{password}';") #Run the query in DB

    if result: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        req.session["type"]= user_type
        return HttpResponseRedirect(f'../{user_type}') #Redirect user to home page
    else:
        return HttpResponseRedirect('../loginIndex?fail=true')

def logout(req):
    if req.session:
        req.session.flush()

    return HttpResponseRedirect('/dbmanagement/') #Redirect user to home page
