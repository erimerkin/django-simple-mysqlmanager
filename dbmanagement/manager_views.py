from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .db_utils import run_statement
from django.shortcuts import redirect

def authenticate(req):
    # if req.session:
    #     if "type" in req.session:
    #         user_type = req.session["type"]
    #         if (user_type != 2):
    #             return redirect('/dbmanagement/')
    return True

def manager_login(req):
    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"SELECT * FROM DBManager WHERE username='{username}' and password='{password}';") #Run the query in DB

    if result: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        req.session["type"]=2
        return HttpResponseRedirect('../home') #Redirect user to home page
    else:
        return HttpResponseRedirect('../login?fail=true')


def removeStudent(req):
    #Retrieve data from the request body
    studentId=req.POST["StudentID"]
    # logged_user=req.session["username"]
    try:
        print(run_statement(f"DELETE FROM Students WHERE Students.student_id = {studentId};"))
        return HttpResponseRedirect("../manager/liststudents")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../manager/liststudents?fail=true')


def addStudent(req):
    #Retrieve data from the request body
    studentId=req.POST["student_id"]
    username = req.POST["username"]
    name = req.POST["name"]
    surname = req.POST["surname"]
    email = req.POST["email"]
    password = req.POST["password"]
    department = req.POST["department"]

    # logged_user=req.session["username"]
    try:
        print(run_statement(f"""INSERT INTO Students(`username`, `name`, `surname`, `email`, `password`, `department_id`, `student_id`, `credits`, `GPA`)
        VALUES('{username}', '{name}', '{surname}', '{email}', '{password}', '{department}', '{studentId}', 0, 0);"""))
        return HttpResponseRedirect("../manager/liststudents")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../manager/addstudent?fail=true')

def addInstructor(req):
    #Retrieve data from the request body
    title=req.POST["title"]
    username = req.POST["username"]
    name = req.POST["name"]
    surname = req.POST["surname"]
    email = req.POST["email"]
    password = req.POST["password"]
    department = req.POST["department"]

    print(title)
    # logged_user=req.session["username"]
    try:
        print(run_statement(f"""INSERT INTO Instructors(`username`, `name`, `surname`, `email`, `password`, `department_id`, `title`)
        VALUES('{username}', '{name}', '{surname}', '{email}', '{password}', '{department}', '{title}');"""))
        return HttpResponseRedirect("../manager/listinstructors")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../manager/addinstructor?fail=true')

### Button Actions
def updateTitle(req):
    #Retrieve data from the request body
    title=req.POST["title"]
    username = req.POST["username"]

    print(title)
    # logged_user=req.session["username"]
    try:
        print(run_statement(f"""UPDATE Instructors 
                                SET title = "{title}"
                                WHERE Instructors.username = "{username}";"""))
        return HttpResponseRedirect("../manager/listinstructors")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../manager/listinstructors?fail=true')



##### STATIC PAGE VIEWS


def home(req):
    if authenticate(req):
        isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
        return render(req,'managerIndex.html')
    else:
        return HttpResponseRedirect("..")

def liststudents(req):
    if authenticate(req):

        result=run_statement(f"SELECT `username`, `name`, `surname`, `email`, `department_id`, `credits`, `gpa` FROM Students ORDER BY `credits` ASC;") #Run the query in DB
        
        # username=req.session["username"] #Retrieve the username of the logged-in user
        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False

        return render(req,'studentList.html',{"results":result,"action_fail":isFailed})
    else:
        return HttpResponseRedirect("..")


def listInstructors(req):
    if authenticate(req):

        result=run_statement(f"""SELECT `username`, `name`, `surname`, `email`, `department_id`, `title` 
                        FROM Instructors;""")
        add_form=UpdateTitleForm()

        # username=req.session["username"] #Retrieve the username of the logged-in user
        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False

        return render(req,'listInstructors.html',{"add_form":add_form, "results":result,"action_fail":isFailed})
    else:
        return HttpResponseRedirect("..")

def page_add_student(req):
    if authenticate(req):

        studentForm = AddStudentForm()
        
        isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
        return render(req,'addStudent.html',{"add_form":studentForm, "action_fail":isFailed})
    else:
        return HttpResponseRedirect("..")

def page_add_instr(req):
    if authenticate(req):
        instrForm = AddInstructorForm()
        
        isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
        return render(req,'addInstructor.html',{"add_form":instrForm, "action_fail":isFailed})
    else:
        return HttpResponseRedirect("..")


# def viewGrade(req):
#     result=run_statement(f"""SELECT `Has_Grade.course_id`, `Course.name` 
#                         FROM `Has_Grade` 
#                         INNER JOIN `Course` ON `Course.course_id` = `Has_Grade.course_id`
#                         WHERE `Has_Grade.username` = (SELECT `username` FROM `Students` WHERE `student_id` = "given_id");""") #Run the query in DB
    
#     add_form = SearchForm()

#     isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False

#     return render(req,'viewGrades.html',{"add_form":add_form, "results":result,"action_fail":isFailed})

def page_viewCourses(req):
    add_form = CustomSearchForm()
    return render(req,'viewCourses.html',{"add_form":add_form})

def page_viewGrades(req):
    add_form = CustomSearchForm()
    return render(req,'viewGrades.html',{"add_form":add_form})

def viewCourse(req):

    #Retrieve data from the request body
    search=req.POST["search_text"]

    try:
        result = run_statement(f"""SELECT `course_id`, `name`, `Given_At.classroom_id`, `Classroom.campus`, `Given_At.timeslot`
                FROM Course
                INNER JOIN `Given_At` ON `Given_At.course_id` = `course_id`
                INNER JOIN `Classroom` ON `Classroom.classroom_id` = `Given_At.classroom_id`
                WHERE `instr_username` = "{search}";""")

        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        return render(req,'viewCourses.html',{"results":result,"action_fail":isFailed})
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../manager/viewcourses?fail=true')
    
    
def page_courseaverage(req):
    add_form = CustomSearchForm()
    return render(req,'courseAverage.html',{"add_form":add_form})

def viewGrade(req):

    #Retrieve data from the request body
    search=req.POST["search_text"]

    try:
        result = run_statement(f"""SELECT `Has_Grade.course_id`, `Course.name` 
                FROM `Has_Grade` 
                INNER JOIN `Course` ON `Course.course_id` = `Has_Gradecourse_id`
                WHERE `username` = (SELECT `username` FROM `Students` WHERE `student_id` = "{search}");""")

        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        return render(req,'viewGrades.html',{"results":result,"action_fail":isFailed})
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../manager/viewgrades?fail=true')



def courseAverage(req):
   #Retrieve data from the request body
    search=req.POST["search_text"]

    try:
        result = run_statement(f"""SELECT `course_id`, `Course.name`, AVG(`grade`) 
                FROM `Has_Grade` 
                INNER JOIN `Course` ON `Course.course_id` = `course_id`
                WHERE `course_id` = "{search}";""")

        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        return render(req,'courseAverage.html',{"results":result,"action_fail":isFailed})
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../manager/courseaverage?fail=true')

 