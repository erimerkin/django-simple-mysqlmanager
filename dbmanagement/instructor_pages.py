from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .utilities import *
from django.shortcuts import redirect

def instr_auth(req):
    if req.session:
        if "type" in req.session:
            user_type = req.session["type"]
            if (user_type == 1):
                return True

    req.session.flush()
    return False

# Homepage function
def home(req):
    if instr_auth(req):
        return render(req,'instructor/instructorIndex.html')
    else:
        return HttpResponseRedirect("./instructor/login")

# Login Page Function
def page_login(req):
    if instr_auth(req):
        return HttpResponseRedirect("../instructor")
    else:
        login_form = UserLoginForm()
        isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
        info_text="Please, login before continuing."

        return render(req,'instructor/login.html', {"add_form":login_form, "action_fail":isFailed, "info_text":info_text})

# Add Course Page
def page_addCourse(req):
    if instr_auth(req):
        
        add_form = AddNewCourseForm()
        info_text = "Please fill the fields to create a new course."

        # username=req.session["username"] #Retrieve the username of the logged-in user
        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        isSuccess=req.GET.get("success",False) #Try to retrieve GET parameter "fail", if it's not given set it to False

        return render(req,'instructor/addCourse.html',{"action_fail":isFailed, "action_success":isSuccess, "add_form":add_form, "info_text":info_text})
    else:
        return HttpResponseRedirect("./login")

# Add Prerequisite Page
def page_addPrerequisite(req):
    if instr_auth(req):
        
        add_form = AddPrerequisiteForm()
        info_text = "You can add prerequisite to a course given"

        # username=req.session["username"] #Retrieve the username of the logged-in user
        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        isSuccess=req.GET.get("success",False) #Try to retrieve GET parameter "fail", if it's not given set it to False

        return render(req,'instructor/addPrerequisite.html',{"action_fail":isFailed, "action_success":isSuccess, "add_form":add_form, "info_text":info_text})
    else:
        return HttpResponseRedirect("./login")

#Update Course Name page
def page_updateCourseName(req):
    if instr_auth(req):
        
        add_form = UpdateCourseNameForm()
        info_text = "You can update name of the course."

        # username=req.session["username"] #Retrieve the username of the logged-in user
        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        isSuccess=req.GET.get("success",False) #Try to retrieve GET parameter "fail", if it's not given set it to False

        return render(req,'instructor/updateCourseName.html',{"action_fail":isFailed, "action_success":isSuccess, "add_form":add_form, "info_text":info_text})
    else:
        return HttpResponseRedirect("./login")

# View Given Courses Page 
def page_viewCoursesGiven(req):
    if instr_auth(req):

        username = req.session["username"]
        info_text = "Lists all courses given by you"

        header_list = ("Course_ID", "Name", "Instructor Surname", "Department", "Credits", "Classroom", "Timeslot", "Quota", "Prerequisites")
        result = run_statement(f"""SELECT Course.`course_id`, Course.`name`, Instructors.`surname`, Instructors.`department_id`, Course.`credits`, Given_At.`classroom_id`, Given_At.`time_slot`, Course.`quota` 
                                FROM Course
                                INNER JOIN Instructors ON Instructors.`username` = Course.`instr_username`
                                INNER JOIN Given_At ON Given_At.`course_id` = Course.`course_id`
                                WHERE Course.`instr_username` = "{username}"
                                ORDER BY Course.`course_id` ASC;""")

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

        return render(req,'instructor/instructorBase.html',{"results":new_result, "headers":header_list, "info_text":info_text})
    else:
        return HttpResponseRedirect("../instructor/login")

# List Student taking a course page
def page_listStudentsForCourse(req):
    if instr_auth(req):

        add_form = CustomSearchForm()
        info_text = "Enter a course id to find students enrolled."

        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        isSuccess=req.GET.get("search",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        header_list = ("Username", "Student ID", "Email", "Student Name", "Student Surname")
        result= False
        if (isSuccess):
            result = run_statement(f"""SELECT Students.`username`, Students.`student_id`, Students.`email`, Students.`name`, Students.`surname`
                                        FROM Students
                                        INNER JOIN Taken ON Taken.`course_id` = "{isSuccess}"
                                        WHERE Taken.`username` = Students.`username`;""")
     

        return render(req,'instructor/listStudentsForCourse.html',{"results":result, "action_fail":isFailed, "add_form":add_form, "info_text":info_text, "headers":header_list, "username":isSuccess})
    else:
        return HttpResponseRedirect("./login")

# Grade a Student page
def page_giveGrade(req):
    if instr_auth(req):
        
        add_form = GiveGradeForm()
        info_text = "You can assign grades to students taking the course"

        # username=req.session["username"] #Retrieve the username of the logged-in user
        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        isSuccess=req.GET.get("success",False) #Try to retrieve GET parameter "fail", if it's not given set it to False

        return render(req,'instructor/giveGrade.html',{"action_fail":isFailed, "action_success":isSuccess, "add_form":add_form, "info_text":info_text})
    else:
        return HttpResponseRedirect("./login")

# List Classrooms for timeslot page
def page_listAllClassrooms(req):
    if instr_auth(req):

        add_form = CustomSearchForm()
        info_text = "Enter a timeslot to search available classrooms."

        isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        isSuccess=req.GET.get("search",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
        header_list = ("Classroom", "Campus", "Capacity")
        result = False
        if (isSuccess):
            result = run_statement(f"""SELECT DISTINCT Given_At.`classroom_id`, Classroom.`campus`, Classroom.`capacity`
                                    FROM Classroom
                                    INNER JOIN Given_At ON (Given_At.`classroom_id` = Classroom.`classroom_id`) 
                                    WHERE Given_At.`classroom_id` NOT IN (SELECT `classroom_id` FROM Given_At WHERE `time_slot` = {isSuccess});""")
     

        return render(req,'instructor/listClassrooms.html',{"results":result, "action_fail":isFailed, "add_form":add_form, "info_text":info_text, "headers":header_list, "username":isSuccess})
    else:
        return HttpResponseRedirect("./login")
