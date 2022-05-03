from django.urls import include, path

from . import views
from . import manager_actions
from . import manager_pages
from . import student_pages
from . import student_actions
from . import instructor_pages
from . import instructor_actions

urlpatterns = [
    path('', views.index, name='index'),
    path('manager', manager_pages.home, name='managerHome'),
    path('manager/login', manager_pages.page_login, name='page_managerLogin'),
    path('manager/addStudent', manager_pages.page_addStudent, name="page_addStudent"),
    path('manager/listStudents', manager_pages.page_listStudents, name="page_listStudents"),
    path('manager/viewGrades', manager_pages.page_viewGrades, name="page_viewGrades"),
    path('manager/removeStudent', manager_pages.page_removeStudent, name="page_removeStudent"),
    path('manager/addInstructor', manager_pages.page_addInstructor, name="page_addInstructor"),
    path('manager/listInstructors', manager_pages.page_listInstructors, name="page_listInstructors"),
    path('manager/viewCourses', manager_pages.page_viewCourses, name="page_viewCourses"),
    path('manager/updateTitle', manager_pages.page_updateTitle, name="page_updateTitle"),
    path('manager/courseAverage', manager_pages.page_courseAverage, name="page_courseAverage"),

    path('manager/actionAddStudent', manager_actions.action_addStudent, name="addStudent"),
    path('manager/actionViewGrades', manager_actions.action_viewGrades, name="viewGrades"),
    path('manager/actionRemoveStudent', manager_actions.action_removeStudent, name="removeStudent"),
    path('manager/actionLogin', manager_actions.action_login, name='managerLogin'),
    path('manager/actionAddInstructor', manager_actions.action_addInstructor, name="addInstructor"),
    path('manager/actionUpdateTitle', manager_actions.action_updateTitle, name="updateTitle"),
    path('manager/actionViewCourses', manager_actions.action_viewCourses, name="viewCourses"),
    path('manager/actionCourseAverage', manager_actions.action_courseAverage, name="courseAverage"),

    path('student', student_pages.home, name="studentHome"),
    path('student/login', student_pages.page_login, name="page_studentLogin"),
    path('student/listAllCourses', student_pages.page_filterCourses, name="page_listAllCourses"),
    path('student/addCourse', student_pages.page_addCourse, name="page_addCourse"),
    path('student/listTakenCourses', student_pages.page_listTakenCourses, name="page_listTakenCourses"),
    path('student/searchCourses', student_pages.page_searchCourses, name="page_searchCourses"),

    path('student/actionLogin', student_actions.action_login, name="studentLogin"),
    path('student/actionAddCourse', student_actions.action_addCourse, name="addCourse"),
    path('student/actionSearchCourses', student_actions.action_searchCourses, name="searchCourses"),
    path('student/actionFilterCourses', student_actions.action_filterCourses, name="filterCourses"),

    path('instructor', instructor_pages.home, name="instructorHome"),
    path('instructor/login', instructor_pages.page_login, name="page_instructorLogin"),
    path('instructor/addCourse', instructor_pages.page_addCourse, name="page_instructorAddCourse"),
    path('instructor/addPrerequisite', instructor_pages.page_addPrerequisite, name="page_addPrerequisite"),
    path('instructor/updateCourseName', instructor_pages.page_updateCourseName, name="page_updateCourseName"),
    path('instructor/viewCoursesGiven', instructor_pages.page_viewCoursesGiven, name="page_viewCoursesGiven"),
    path('instructor/listStudentsForCourse', instructor_pages.page_listStudentsForCourse, name="page_listStudentsForCourse"),
    path('instructor/giveGrade', instructor_pages.page_giveGrade, name="page_giveGrade"),
    path('instructor/listAllClassrooms', instructor_pages.page_listAllClassrooms, name="page_listAllClassrooms"),

    path('instructor/actionLogin', instructor_actions.action_login, name="instructorLogin"),
    path('instructor/actionAddCourse', instructor_actions.action_addCourse, name="instructorAddCourse"),
    path('instructor/actionAddPrerequisite', instructor_actions.action_addPrerequisite, name="addPrerequisite"),
    path('instructor/actionUpdateCourseName', instructor_actions.action_updateCourseName, name="updateCourseName"),
    path('instructor/actionListStudentsForCourse', instructor_actions.action_listStudentsForCourse, name="listStudentsForCourse"),
    path('instructor/actionGiveGrade', instructor_actions.action_giveGrade, name="giveGrade"),
    path('instructor/actionListAllClassrooms', instructor_actions.action_listAllClassrooms, name="listAllClassrooms"),

    path('logout', views.logout, name="logout"),
]