from django import forms

class UserLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password=forms.CharField(widget=forms.PasswordInput)

class CustomSearchForm(forms.Form):
    search = forms.CharField()

class AddCourseForm(forms.Form):
    course_ID = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Course ID'}))

class FilterForm(forms.Form):
    department_id=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'department id'}))
    campus=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Campus'}))
    minimum_credit=forms.IntegerField(widget=forms.TextInput)
    maximum_credit=forms.IntegerField(widget=forms.TextInput)

class AddNewCourseForm(forms.Form):
    course_id=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Course ID'}))
    course_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name'}))
    course_credits=forms.IntegerField(widget=forms.TextInput)
    classroom_id=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Classroom ID'}))
    timeslot=forms.IntegerField(widget=forms.TextInput)
    quota=forms.IntegerField(widget=forms.TextInput)

class AddPrerequisiteForm(forms.Form):
    course_id=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Course ID'}))
    prerequisite_id=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Prerequisite Course ID'}))

class UpdateCourseNameForm(forms.Form):
    course_id=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Course ID'}))
    course_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Course Name'}))

class GiveGradeForm(forms.Form):
    course_id=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Course ID'}))
    student_id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'Student ID'}))
    grade=forms.IntegerField(widget=forms.TextInput)


class RemoveStudentForm(forms.Form):
    student_id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'Student ID'}))

class AddStudentForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password=forms.CharField(widget=forms.PasswordInput)
    name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name'}))
    surname=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Surname'}))
    email=forms.EmailField()
    department=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'department id'}))
    student_id=forms.IntegerField(widget=forms.TextInput)


class AddInstructorForm(forms.Form):
    instr_titles = [("Assistant Professor", "Assistant Professor"), ("Associate Professor","Associate Professor"), ("Professor","Professor")]
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password=forms.CharField(widget=forms.PasswordInput)
    name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name'}))
    surname=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Surname'}))
    email=forms.EmailField()
    department=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'department id'}))
    title=forms.ChoiceField(choices=instr_titles)

class UpdateTitleForm(forms.Form):
    instr_titles = [("Assistant Professor", "Assistant Professor"), ("Associate Professor","Associate Professor"), ("Professor","Professor")]
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    title=forms.ChoiceField(choices=instr_titles)

