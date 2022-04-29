from django.urls import path

from . import views
from . import manager_views

urlpatterns = [
    path('', views.index, name='index'),
    path('instructor', views.instructor, name='instructor'),
    path('student', views.student_login, name='student'),
    path('manager', manager_views.home, name='managerHome'),
    path('manager/liststudents', manager_views.liststudents, name="listStudents"),
    path('manager/removeStudent', manager_views.removeStudent, name="removeStudent"),
    path('manager/addstudent', manager_views.page_add_student, name="addStudentPage"),
    path('manager/actionAddStudent', manager_views.addStudent, name="addStudent"),
    path('manager/addinstructor', manager_views.page_add_instr, name="addInstructorPage"),
    path('manager/actionAddInstructor', manager_views.addInstructor, name="addInstructor"),
    path('manager/listinstructors', manager_views.listInstructors, name="listInstructor"),
    path('manager/updateTitle', manager_views.updateTitle, name="updateTitle"),
    path('manager/back', manager_views.home, name="goBack"),
    path('logout', views.logout, name="logout"),
    path('manager/viewcourses', manager_views.page_viewCourses, name="pageViewCourses"),
    path('manager/actionViewCourse', manager_views.viewCourse, name="viewCourse"),
       path('manager/viewgrades', manager_views.page_viewGrades, name="pageViewGrades"),
    path('manager/courseaverage', manager_views.page_courseaverage, name="pageCourseAverage"),
    path('manager/actionViewGrade', manager_views.viewGrade, name="viewGrade"),
    path('manager/actionCourseAverage', manager_views.courseAverage, name="courseAverage"),
]