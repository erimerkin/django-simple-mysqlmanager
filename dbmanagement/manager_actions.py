from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .utilities import *
from django.shortcuts import redirect

# Function to handle login process
def action_login(req):
    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"""SELECT * FROM DBManager WHERE `username`="{username}" AND `password`="{encrypt_password(password)}";""") #Run the query in DB
    print(result)
    if result: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        req.session["type"]=2
        return HttpResponseRedirect('../manager') #Redirect user to home page
    else:
        return HttpResponseRedirect('../manager/login?fail=true')

# Function that removes given student 
def action_removeStudent(req):
    #Retrieve data from the request body
    studentId=req.POST["student_id"]
    try:
        if (run_statement(f"""SELECT `student_id` FROM Students WHERE Students.`student_id` = {studentId}""")):
            print(run_statement(f"DELETE FROM Students WHERE Students.student_id = {studentId};"))
            return HttpResponseRedirect(f"../manager/removeStudent?success={studentId}")
        
        return HttpResponseRedirect(f'../manager/removeStudent?fail={studentId}')

    except Exception as e:
        print(str(e))
        return HttpResponseRedirect(f'../manager/removeStudent?fail={studentId}')

# Function that adds new students according to given info
def action_addStudent(req):
    #Retrieve data from the request body
    studentId=req.POST["student_id"]
    username = req.POST["username"]
    name = req.POST["name"]
    surname = req.POST["surname"]
    email = req.POST["email"]
    password = encrypt_password(req.POST["password"])
    department = req.POST["department"]

    try:
        print(run_statement(f"""INSERT INTO Students(`username`, `name`, `surname`, `email`, `password`, `department_id`, `student_id`, `credits`, `GPA`)
        VALUES('{username}', '{name}', '{surname}', '{email}', '{password}', '{department}', '{studentId}', 0, 0);"""))
        return HttpResponseRedirect("../manager/addStudent?success=true")
    except Exception as e:
        return HttpResponseRedirect(f'../manager/addStudent?fail={str(e)}')

# Function that adds new instructor according to given info
def action_addInstructor(req):
    #Retrieve data from the request body
    title=req.POST["title"]
    username = req.POST["username"]
    name = req.POST["name"]
    surname = req.POST["surname"]
    email = req.POST["email"]
    password = encrypt_password(req.POST["password"])
    department = req.POST["department"]

    try:
        print(run_statement(f"""INSERT INTO Instructors(`username`, `name`, `surname`, `email`, `password`, `department_id`, `title`)
        VALUES('{username}', '{name}', '{surname}', '{email}', '{password}', '{department}', '{title}');"""))
        return HttpResponseRedirect("../manager/addInstructor?success=true")
    except Exception as e:
        return HttpResponseRedirect(f'../manager/addInstructor?fail={str(e)}')

# Function that activates and updates the title according to given info
def action_updateTitle(req):

    #Retrieve data from the request body
    title=req.POST["title"]
    username = req.POST["username"]

    try:
        if(run_statement(f"""SELECT `username` FROM Instructors WHERE `username` = "{username}" """)):
            print(run_statement(f"""UPDATE Instructors 
                                    SET title = "{title}"
                                    WHERE Instructors.username = "{username}";"""))
            return HttpResponseRedirect(f"../manager/updateTitle?success={username}")
        else:
            return HttpResponseRedirect(f'../manager/updateTitle?fail={username}')
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect(f'../manager/updateTitle?fail={username}')

# Function that redirects the search text to view for listing average of a given course
def action_courseAverage(req):
#Retrieve data from the request body
    search_text=req.POST["search"]

    try:
        if(run_statement(f"""SELECT `course_id` FROM Course WHERE `course_id` = "{search_text}" """)):
            return HttpResponseRedirect(f"../manager/courseAverage?search={search_text}")
        else:
            return HttpResponseRedirect(f'../manager/courseAverage?fail={search_text}')
    except Exception as e:
        return HttpResponseRedirect(f'../manager/courseAverage?fail={search_text}')
          


# Function that redirects the search text to view for viewing all courses of an instructor
def action_viewCourses(req):

    #Retrieve data from the request body
    search_text=req.POST["search"]

    try:
        if(run_statement(f"""SELECT `username` FROM Instructors WHERE `username` = "{search_text}" """)):
            return HttpResponseRedirect(f"../manager/viewCourses?search={search_text}")
        else:
            return HttpResponseRedirect(f'../manager/viewCourses?fail={search_text}')
    except Exception as e:
        return HttpResponseRedirect(f'../manager/viewCourses?fail={search_text}')
    
# Function that redirects the search text to viewing all grades of a student
def action_viewGrades(req):

    #Retrieve data from the request body
    search_text=req.POST["search"]

    try:
        if(run_statement(f"""SELECT `student_id` FROM Students WHERE `student_id` = {search_text}""")):
            return HttpResponseRedirect(f"../manager/viewGrades?search={search_text}")
        else:
            return HttpResponseRedirect(f'../manager/viewGrades?fail={search_text}')
    except Exception as e:
        return HttpResponseRedirect(f'../manager/viewGrades?fail={search_text}')

