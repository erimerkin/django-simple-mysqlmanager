from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .utilities import *
from django.shortcuts import redirect

def action_login(req):
    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"""SELECT * FROM Instructors WHERE `username`="{username}" AND `password`="{encrypt_password(password)}";""") #Run the query in DB
    if result: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        req.session["type"]=1
        return HttpResponseRedirect('../instructor') #Redirect user to home page
    else:
        return HttpResponseRedirect('../instructor/login?fail=true')

def action_listAllClassrooms(req):
    #Retrieve data from the request body
    search_text=req.POST["search"]
    try:
        return HttpResponseRedirect(f'../instructor/listAllClassrooms?search={search_text}')
    except Exception as e:
        return HttpResponseRedirect(f'../instructor/listAllClassrooms?fail={str(e)}')

def action_listStudentsForCourse(req):
    #Retrieve data from the request body
    search_text=req.POST["search"]
    instr_username=req.session["username"]
    try:
        if (run_statement(f"""SELECT * FROM Course WHERE `course_id` = "{search_text}" AND `instr_username` = "{instr_username}"; """)):
            return HttpResponseRedirect(f'../instructor/listStudentsForCourse?search={search_text}')
        else:
            return HttpResponseRedirect(f'../instructor/listStudentsForCourse?fail="You do not give this course."')

    except Exception as e:
        return HttpResponseRedirect(f'../instructor/listStudentsForCourse?fail={str(e)}')

def action_addCourse(req):
    course_id=req.POST["course_id"]
    classroom_id=req.POST["classroom_id"]
    course_credits=req.POST["course_credits"]
    course_name=req.POST["course_name"]
    course_quota=req.POST["quota"]
    timeslot = req.POST["timeslot"]

    instr_username=req.session["username"]
    try:
        run_statement(f"""INSERT INTO Course(`course_id`, `credits`, `name`, `quota`, `instr_username`)  VALUES("{course_id}", {course_credits}, "{course_name}", {course_quota}, "{instr_username}");""") 
        run_statement(f"""INSERT INTO Given_At(`course_id`, `classroom_id`, `time_slot`)  VALUES("{course_id}", "{classroom_id}", {timeslot});""")

        if (len(run_statement(f"""SELECT `capacity` FROM Classroom WHERE `classroom_id` = "{classroom_id}" AND `capacity` >= {course_quota}; """)) == 0):
            return HttpResponseRedirect(f"../instructor/addCourse?fail='Classroom capacity is insufficient for this course.'")

        return HttpResponseRedirect(f"../instructor/addCourse?success=true")
    except Exception as e:
        return HttpResponseRedirect(f'../instructor/addCourse?fail={str(e)}')

def action_addPrerequisite(req):
    course_id=req.POST["course_id"]
    prereq_id=req.POST["prerequisite_id"]
    instr_username=req.session["username"]
    try:
        if (run_statement(f"""SELECT * FROM Course WHERE Course.`course_id` = "{course_id}" AND Course.`instr_username` = "{instr_username}"; """)):
            run_statement(f"""INSERT INTO Has_Prerequisite(`course_id`, `prereq_id`)  VALUES("{course_id}", "{prereq_id}");""")
            return HttpResponseRedirect(f"../instructor/addPrerequisite?success=true")
        else:
            return HttpResponseRedirect(f"../instructor/addPrerequisite?fail='This course is not given by you.'")
    except Exception as e:
        return HttpResponseRedirect(f'../instructor/addPrerequisite?fail={str(e)}')

def action_updateCourseName(req):
    course_id=req.POST["course_id"]
    updated_name=req.POST["course_name"]
    instr_username=req.session["username"]
    try:
        if (run_statement(f"""SELECT * FROM Course WHERE Course.`course_id` = "{course_id}" AND Course.`instr_username` = "{instr_username}"; """)):
            run_statement(f"""UPDATE Course
                            SET Course.`name` = "{updated_name}"
                            WHERE (Course.`course_id` = "{course_id}") AND (Course.`instr_username` = "{instr_username}");;""")
            return HttpResponseRedirect(f"../instructor/updateCourseName?success=true")
        else:
            return HttpResponseRedirect(f"../instructor/updateCourseName?fail='This course is not given by you.'")
    except Exception as e:
        return HttpResponseRedirect(f'../instructor/updateCourseName?fail={str(e)}')

def action_giveGrade(req):
    course_id=req.POST["course_id"]
    student_id=req.POST["student_id"]
    grade=req.POST["grade"]
    instr_username=req.session["username"]
    try:
        if (run_statement(f"""SELECT * FROM Course WHERE Course.`course_id` = "{course_id}" AND Course.`instr_username` = "{instr_username}"; """)):
            
            if (run_statement(f"""SELECT * FROM Taken 
                                INNER JOIN Students ON Taken.`username` = Students.`username`
                                WHERE Taken.`course_id` = "{course_id}" AND Students.`student_id`= {student_id};""")):

                student_username = run_statement(f"""SELECT `username` FROM Students WHERE `student_id` = {student_id};""")
                for item in student_username:
                    for student in item:
                        run_statement(f"""INSERT INTO Has_Grade(`student_username`, `course_id`, `grade`) VALUES("{student}", "{course_id}", {grade}); """)

                return HttpResponseRedirect(f"../instructor/giveGrade?success=true")
            else:
                return HttpResponseRedirect(f"../instructor/giveGrade?fail='This student doesn't take this course.'")
        else:
            return HttpResponseRedirect(f"../instructor/giveGrade?fail='This course is not given by you.'")
    except Exception as e:
        return HttpResponseRedirect(f'../instructor/giveGrade?fail={str(e)}')