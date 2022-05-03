from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .utilities import *
from django.shortcuts import redirect

def action_login(req):
    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"""SELECT * FROM Students WHERE `username`="{username}" AND `password`="{encrypt_password(password)}";""") #Run the query in DB
    if result: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        req.session["type"]=0
        return HttpResponseRedirect('../student') #Redirect user to home page
    else:
        return HttpResponseRedirect('../student/login?fail=true')

def action_addCourse(req):
    #Retrieve data from the request body
    course_id=req.POST["course_ID"]
    username = req.session["username"]
    try:
        run_statement(f"""INSERT INTO Taken(`username`, `course_id`)  VALUES("{username}", "{course_id}");""")
        return HttpResponseRedirect(f"../student/addCourse?success=true")
    
    except Exception as e:
        return HttpResponseRedirect(f'../student/addCourse?fail={str(e)}')

def action_searchCourses(req):
    #Retrieve data from the request body
    search_text=req.POST["search"]

    try:
        return HttpResponseRedirect(f'../student/searchCourses?search={search_text}')
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect(f'../student/searchCourses?fail={search_text}')

def action_filterCourses(req):
    department_id=req.POST["department_id"]
    campus=req.POST["campus"]
    min_cred=req.POST["minimum_credit"]
    max_cred=req.POST["maximum_credit"]

    try:
        return HttpResponseRedirect(f'../student/listAllCourses?department={department_id}&campus={campus}&min={min_cred}&max={max_cred}')
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect(f'../student/listAllCourses?fail={str(e)}')