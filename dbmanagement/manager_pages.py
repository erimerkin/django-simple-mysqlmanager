from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .utilities import *
from django.shortcuts import redirect

# authenticate function
def authenticate(req):
    if req.session:
        if "type" in req.session:
            user_type = req.session["type"]
            if (user_type == 2):
                print(req.session["username"])
                return True

    req.session.flush()
    return False


##### STATIC PAGE VIEWS

# Home page
def home(req):
    if authenticate(req):
        return render(req,'manager/managerIndex.html')
    else:
        return HttpResponseRedirect("./manager/login")

# Page to handle login
def page_login(req):
    if authenticate(req):
        return HttpResponseRedirect("../manager")
    else:
        login_form = UserLoginForm()
        isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
        info_text="Please, login before continuing."

        return render(req,'manager/login.html', {"add_form":login_form, "action_fail":isFailed, "info_text":info_text})

# Page to list all students
def page_listStudents(req):
    if authenticate(req):

        result=run_statement(f"SELECT `username`, `name`, `surname`, `email`, `department_id`, `credits`, `gpa` FROM Students ORDER BY `credits` ASC;") #Run the query in DB
        
        header_list = ("Username", "Name", "Surname", "Email", "Department", "Completed Credits", "GPA")

        # username=req.session["username"] #Retrieve the username of the logged-in user
        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False

        return render(req,'manager/listStudents.html',{"results":result,"action_fail":isFailed, "headers":header_list})
    else:
        return HttpResponseRedirect("../manager/login")

# Page to list all instructors
def page_listInstructors(req):
    if authenticate(req):

        result=run_statement(f"""SELECT `username`, `name`, `surname`, `email`, `department_id`, `title` 
                        FROM Instructors;""")

        header_list = ("Username", "Name", "Surname", "Email", "Department", "Title")
        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False

        return render(req,'manager/listInstructors.html',{"results":result,"action_fail":isFailed, "headers":header_list})
    else:
        return HttpResponseRedirect("../manager/login")

# Page to update title of an existing instructor
def page_updateTitle(req):
    if authenticate(req):
        
        add_form = UpdateTitleForm()
        info_text = "To update title of an instructor please enter their username and select a title."

        # username=req.session["username"] #Retrieve the username of the logged-in user
        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        isSuccess=req.GET.get("success",False) #Try to retrieve GET parameter "fail", if it's not given set it to False


        return render(req,'manager/updateTitle.html',{"action_fail":isFailed, "action_success":isSuccess, "add_form":add_form, "info_text":info_text})
    else:
        return HttpResponseRedirect("./login")

# Page to remove a student
def page_removeStudent(req):
    if authenticate(req):

        add_form = RemoveStudentForm()
        info_text = "Enter the StudentID of student you want to delete."


        # username=req.session["username"] #Retrieve the username of the logged-in user
        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        isSuccess=req.GET.get("success",False) #Try to retrieve GET parameter "fail", if it's not given set it to False


        return render(req,'manager/removeStudent.html',{"action_fail":isFailed, "action_success":isSuccess, "add_form":add_form, "info_text":info_text})
    else:
        return HttpResponseRedirect("./login")

# Page to add a new student
def page_addStudent(req):
    if authenticate(req):

        studentForm = AddStudentForm()
        
        isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
        isSuccess=req.GET.get("success", False)
        info_text= "Please fill the details for a new student."
        return render(req,'manager/addStudent.html',{"add_form":studentForm, "action_fail":isFailed, "action_success":isSuccess, "info_text":info_text})
    else:
        return HttpResponseRedirect("../manager/login")

# Page to add a new instructor
def page_addInstructor(req):
    if authenticate(req):

        instrForm = AddInstructorForm()
        
        isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
        isSuccess=req.GET.get("success", False)
        info_text= "Please fill the details for a new instructor."
        return render(req,'manager/addInstructor.html',{"add_form":instrForm, "action_fail":isFailed, "action_success":isSuccess, "info_text":info_text})
    else:
        return HttpResponseRedirect("./login")


# Page to view courses of a given instructor
def page_viewCourses(req):
    if authenticate(req):

        add_form = CustomSearchForm()
        info_text = "Enter username of instructor you want to list courses."

        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        isSuccess=req.GET.get("search",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        result = False
        header_list = False
        if (isSuccess):
            print("Test")
            result = run_statement(f"""SELECT Course.`course_id`, Course.`name`, Given_At.`classroom_id`, Classroom.`campus`, Given_At.`time_slot` 
                FROM Course
                INNER JOIN Given_At ON Given_At.`course_id` = Course.`course_id`
                INNER JOIN Classroom ON Classroom.`classroom_id` = Given_At.`classroom_id`
                WHERE Course.`instr_username` = "{isSuccess}";""")
            print(result)
            header_list = ("Course_ID", "Name", "Classroom", "Campus", "Timeslot")

        return render(req,'manager/viewCourses.html',{"results":result, "action_fail":isFailed, "add_form":add_form, "info_text":info_text, "headers":header_list, "username":isSuccess})
    else:
        return HttpResponseRedirect("./login")

# Page to view grades of a given student
def page_viewGrades(req):
    if authenticate(req):

        add_form = CustomSearchForm()
        info_text = "Enter student ID of student you want to list grades of."

        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        isSuccess=req.GET.get("search",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        result = False
        header_list = False
        if (isSuccess):
            print("Test")
            result = run_statement(f"""SELECT Has_Grade.`course_id`, Course.`name`, Has_Grade.`grade`
                        FROM Has_Grade 
                        INNER JOIN Course ON Course.`course_id` = Has_Grade.`course_id`
                        WHERE Has_Grade.`student_username` = (SELECT `username` FROM `Students` WHERE `student_id` = {isSuccess});""")
            header_list = ("Course_ID", "Name", "Grade")

        return render(req,'manager/viewGrades.html',{"results":result, "action_fail":isFailed, "add_form":add_form, "info_text":info_text, "headers":header_list, "username":isSuccess})
    else:
        return HttpResponseRedirect("./login")


# Page showing a given course's average
def page_courseAverage(req):
    if authenticate(req):

        add_form = CustomSearchForm()
        info_text = "Enter course ID of the course you want to list average grades."

        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        isSuccess=req.GET.get("search",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        result = False
        header_list = False
        if (isSuccess):
            result = run_statement(f"""SELECT Course.`course_id`, Course.`name`, AVG(Has_Grade.`grade`) as `Grade_Average`
                                        FROM Course
                                        INNER JOIN Has_Grade ON Has_Grade.`course_id` = "{isSuccess}"
                                        WHERE Course.`course_id` = "{isSuccess}";""")
            header_list = ("Course_ID", "Name", "Average Grade")

        return render(req,'manager/courseAverage.html',{"results":result, "action_fail":isFailed, "add_form":add_form, "info_text":info_text, "headers":header_list, "username":isSuccess})
    else:
        return HttpResponseRedirect("./login")






 