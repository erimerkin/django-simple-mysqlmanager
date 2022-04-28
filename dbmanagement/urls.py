from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('instructor', views.instructor, name='instructor'),
    path('student', views.student_login, name='student'),
    path('manager', views.manager_login, name='manager'),
]