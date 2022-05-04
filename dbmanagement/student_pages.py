from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .utilities import *
from django.shortcuts import redirect

# Authentication Function
def student_auth(req):
    if req.session:
        if "type" in req.session:
            user_type = req.session["type"]
            if (user_type == 0):
                return True

    req.session.flush()
    return False

# Home page
def home(req):
    if student_auth(req):
        return render(req,'student/studentIndex.html')
    else:
        return HttpResponseRedirect("./student/login")

# Login Page
def page_login(req):
    if student_auth(req):
        return HttpResponseRedirect("../student")
    else:
        login_form = UserLoginForm()
        isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
        info_text="Please, login before continuing."

        return render(req,'student/login.html', {"add_form":login_form, "action_fail":isFailed, "info_text":info_text})

# Page that list all taken courses for the current student
def page_listTakenCourses(req):
    if student_auth(req):

        username = req.session["username"]
        info_text = "Lists all previously and currently taken courses for you."

        result = run_statement(f"""SELECT Course.`course_id`, Course.`name`, NULL 
                                    FROM Taken 
                                    INNER JOIN Course ON Course.`course_id` = Taken.`course_id`
                                    WHERE `username` = "{username}"
                                    UNION
                                    SELECT Course.`course_id`, Course.`name`, Has_Grade.`grade` 
                                    FROM Has_Grade 
                                    INNER JOIN Course ON Course.`course_id` = Has_Grade.`course_id`
                                    WHERE `student_username` = "{username}";
                                    """)
                                            
        header_list = ("Course_ID", "Course Name", "Grade")
        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False

        return render(req,'student/studentBase.html',{"results":result,"action_fail":isFailed, "headers":header_list, "info_text":info_text})
    else:
        return HttpResponseRedirect("../student/login")

# Page to add a new course for a student
def page_addCourse(req):
    if student_auth(req):
        
        add_form = AddCourseForm()
        info_text = "Please enter a course id to add it to taken courses."

        # username=req.session["username"] #Retrieve the username of the logged-in user
        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        isSuccess=req.GET.get("success",False) #Try to retrieve GET parameter "fail", if it's not given set it to False

        return render(req,'student/addCourse.html',{"action_fail":isFailed, "action_success":isSuccess, "add_form":add_form, "info_text":info_text})
    else:
        return HttpResponseRedirect("./login")

# Page to search courses containing certain keywords in their name
def page_searchCourses(req):
    if student_auth(req):

        add_form = CustomSearchForm()
        info_text = "Enter a keyword to search course."

        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        isSuccess=req.GET.get("search",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        new_result = False
        header_list = ("Course_ID", "Name", "Instructor Surname", "Department", "Credits", "Classroom", "Timeslot", "Quota", "Prerequisites")
        
        if (isSuccess):

            result = run_statement(f"""SELECT Course.`course_id`, Course.`name`, Instructors.`surname`, Instructors.`department_id`, Course.`credits`, Given_At.`classroom_id`, Given_At.`time_slot`, Course.`quota` 
                                FROM Course
                                INNER JOIN Instructors ON Instructors.`username` = Course.`instr_username`
                                INNER JOIN Given_At ON Given_At.`course_id` = Course.`course_id`
                                WHERE Course.`name` LIKE "%{isSuccess}%";""")

            new_result = []
            for item in result:
                temp_list = list(item)
                prereq_tuple = run_statement(f"""SELECT `prereq_id` FROM Has_Prerequisite WHERE Has_Prerequisite.`course_id` = "{temp_list[0]}" """)
                prereq_list = []
                for pre in prereq_tuple:
                    for pre_item in pre:
                        prereq_list.append(pre_item)

                prereq_string = ", ".join(prereq_list)
                temp_list.append(prereq_string)
                item = tuple(temp_list)
                new_result.append(item)
     

        return render(req,'student/searchCourses.html',{"results":new_result, "action_fail":isFailed, "add_form":add_form, "info_text":info_text, "headers":header_list, "username":isSuccess})
    else:
        return HttpResponseRedirect("./login")

# page to list and filter courses
def page_filterCourses(req):
    if student_auth(req):
        info_text = "Lists all active courses"

        add_form = FilterForm()

        department_id = req.GET.get("department", False)
        campus = req.GET.get("campus", "")
        min_creds = req.GET.get("min", "")
        max_creds = req.GET.get("max", "")

        filtered = False

        header_list = ("Course_ID", "Name", "Instructor Surname", "Department", "Credits", "Classroom", "Timeslot", "Quota", "Prerequisites")
        result = ""

        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False

        if isFailed:
            department_id = False

        if (department_id):
            filtered = True
            try:
                result = run_statement(f"""CALL FilterCourses("{department_id}", "{campus}", {min_creds}, {max_creds}) """)
            except Exception as e:
                return HttpResponseRedirect(f'../student/listAllCourses?fail={str(e)}')

        else:
            result = run_statement(f"""SELECT Course.`course_id`, Course.`name`, Instructors.`surname`, Instructors.`department_id`, Course.`credits`, Given_At.`classroom_id`, Given_At.`time_slot`, Course.`quota` 
                                FROM Course
                                INNER JOIN Instructors ON Instructors.`username` = Course.`instr_username`
                                INNER JOIN Given_At ON Given_At.`course_id` = Course.`course_id`;""")
        

        new_result = []
        for item in result:
            temp_list = list(item)
            prereq_tuple = run_statement(f"""SELECT `prereq_id` FROM Has_Prerequisite WHERE Has_Prerequisite.`course_id` = "{temp_list[0]}" """)
            prereq_list = []
            for pre in prereq_tuple:
                for pre_item in pre:
                    prereq_list.append(pre_item)

            prereq_string = ", ".join(prereq_list)
            temp_list.append(prereq_string)
            item = tuple(temp_list)
            new_result.append(item)
        
        return render(req,'student/listAllCourses.html',{"add_form":add_form,"results":new_result,"action_fail":isFailed, "headers":header_list, "info_text":info_text, "dept":department_id, "campus":campus, "min":min_creds, "max":max_creds, "username":filtered})
    else:
        return HttpResponseRedirect("../student/login")