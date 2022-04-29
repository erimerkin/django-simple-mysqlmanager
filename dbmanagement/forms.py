from django import forms

class UserLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password=forms.CharField(widget=forms.PasswordInput)

class CustomSearchForm(forms.Form):
    search_text = forms.CharField()


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

