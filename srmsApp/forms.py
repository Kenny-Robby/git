from random import choices
import sched
from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm, UserChangeForm

from django.contrib.auth.models import User
from srmsApp import models
from datetime import datetime

class UpdateProfile(UserChangeForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    current_password = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name')

    def clean_current_password(self):
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError(f"Password is Incorrect")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")

class UpdatePasswords(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Confirm New Password")
    class Meta:
        model = User
        fields = ('old_password','new_password1', 'new_password2')

class SaveClass(forms.ModelForm):
    level = forms.CharField(max_length="250")
    course = forms.CharField(max_length="250")
    status = forms.ChoiceField(choices=[('1','Active'),('2','Inctive')])

    class Meta:
        model = models.Class
        fields = ('level','course', 'status',)

    def clean_level(self):
        level = self.cleaned_data['level']
        course = self.data['course']
        id = self.data['id'] if not self.data['id'] == '' else None

        try:
            if id is None:
                levelCount = models.Class.objects.filter(level=level, course=course).count()
            else:
                levelCount = models.Class.objects.exclude(id = id).filter(level=level, course=course).count()
            if levelCount  == 0:
                return level
        except:
            return level
        
        raise forms.ValidationError("Class Already Exists on the list.")



class SaveSubject(forms.ModelForm):
    name = forms.CharField(max_length="250")
    code = forms.CharField(max_length="250", label="Code") #field for module code
    credit = forms.IntegerField(label="Credits", min_value=1)  # Added field for subject credits
    status = forms.ChoiceField(choices=[('1','Active'),('2','Inctive')])

    class Meta:
        model = models.Subject
        fields = ('name','code','credit', 'status',)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        id = self.data['id'] if not self.data['id'] == '' else None
        try:
            if not id is None:
                subjectCount = models.Subject.objects.exclude(id=id).filter(name=name).count()
            else:
                subjectCount = models.Subject.objects.filter(name=name).count()
                print(subjectCount)
            if subjectCount == 0:
                return name
        except Exception as err:
            print(err)
            raise forms.ValidationError("An Error occurred.")
        raise forms.ValidationError("Subject Name Already Exists.")

class SaveStudent(forms.ModelForm):
    classI = forms.CharField(max_length="30", label="Class")
    student_id = forms.CharField(max_length="500", label="Student ID/Code")
    first_name = forms.CharField(max_length="500", label="First Name")
    middle_name = forms.CharField(max_length="500", label="Middle Name", required=False)
    last_name = forms.CharField(max_length="500", label="Last Name")
    birthdate = forms.DateField(label="Birthdate", required=False)
    gender = forms.ChoiceField(choices=[('Male','Male'),('Female','Female')], label="Gender")
    status = forms.ChoiceField(choices = [('1' ,'Active'),('2' ,'Inactive')], label="Status")
    

    class Meta:
        model = models.Student
        fields = ('classI', 'student_id', 'first_name', 'middle_name', 'last_name', 'birthdate', 'gender','status',)
    
    def clean_classI(self):
        class_id = self.cleaned_data['classI']

        try:
            classI = models.Class.objects.get(id = class_id)
            return classI
        except Exception as err:
            print(err)
            raise forms.ValidationError(f"Invalid field value")

    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']
        id = self.data['id'] if not self.data['id'] == '' else None
        try:
            if not id is None:
                studentCount = models.Student.objects.exclude(id = id).filter(student_id=student_id).count()
            else:
                studentCount = models.Student.objects.filter(student_id=student_id).count()
            if studentCount == 0:
                return student_id
        except Exception as err:
            print(err)
            raise forms.ValidationError("An Error occurred.")

        raise forms.ValidationError(f" [{student_id}] Already Exists.")


class SaveResult(forms.ModelForm):
    student = forms.CharField(max_length="30", label="Student")
    semester = forms.CharField(max_length="250", label="Semester")
    
    class Meta:
        model = models.Result
        fields = ('student', 'semester',)
    
    def clean_student(self):
        student = self.cleaned_data['student']
        try:
            studentI = models.Student.objects.get(id = student)
            return studentI
        except Exception as err:
            print(err)
            raise forms.ValidationError(f"Invalid field value")

class SaveSubjectResult(forms.ModelForm):
    result = forms.CharField(max_length="30", label="Result ID")
    subject = forms.CharField(max_length="30", label="Subject")
    score = forms.CharField(max_length="100", label="total")
    

    
    class Meta:
        model = models.Student_Subject_Result
        fields = ('result','subject','score',)
    
    def clean_result(self):
        result = self.cleaned_data['result']

        try:
            resultI = models.Result.objects.get(id = result)
            return resultI
        except Exception as err:
            print(err)
            raise forms.ValidationError(f"Invalid field value")

    def clean_subject(self):
        subject = self.cleaned_data['subject']

        try:
            subjectI = models.Subject.objects.get(id = subject)
            return subjectI
        except Exception as err:
            print(err)
            raise forms.ValidationError(f"Invalid field value")
        

# class SaveResult(forms.ModelForm):
#     student = forms.CharField(max_length="30", label="Student")
#     semester = forms.CharField(max_length="250", label="Semester")
    
#     class Meta:
#         model = models.Result
#         fields = ('student', 'semester',)

# class SaveSubjectResult(forms.ModelForm):
#     result = forms.CharField(max_length="30", label="Result ID")
#     subject = forms.CharField(max_length="30", label="Subject")
#     score = forms.CharField(max_length="100", label="Score")
    
#     class Meta:
#         model = models.Student_Subject_Result
#         fields = ('result','subject','score',)






# class SaveSubjectResult(forms.ModelForm):
#     result = forms.CharField(max_length="30", label="Result ID")
#     subject = forms.CharField(max_length="30", label="Subject")
#     score = forms.CharField(max_length="100", label="Score")
#     grade = forms.CharField(max_length=2, label="Grade", required=False)
#     grade_point = forms.FloatField(label="Grade Point", required=False)
    
#     class Meta:
#         model = models.Student_Subject_Result
#         fields = ('result', 'subject', 'score', 'grade', 'grade_point',)
    
#     def clean_result(self):
#         result = self.cleaned_data['result']

#         try:
#             resultI = models.Result.objects.get(id=result)
#             return resultI
#         except models.Result.DoesNotExist:
#             raise forms.ValidationError("Invalid result ID")
    
#     def clean_subject(self):
#         subject = self.cleaned_data['subject']

#         try:
#             subjectI = models.Subject.objects.get(id=subject)
#             return subjectI
#         except models.Subject.DoesNotExist:
#             raise forms.ValidationError("Invalid subject ID")

#     def clean(self):
#         cleaned_data = super().clean()
#         score = cleaned_data.get('score')

#         if score:
#             try:
#                 score = float(score)
#                 if score >= 70:
#                     cleaned_data['grade'] = 'A'
#                     cleaned_data['grade_point'] = 5.0
#                 elif 60 <= score < 70:
#                     cleaned_data['grade'] = 'B+'
#                     cleaned_data['grade_point'] = 4.0
#                 elif 50 <= score < 60:
#                     cleaned_data['grade'] = 'B'
#                     cleaned_data['grade_point'] = 3.0
#                 elif 40 <= score < 50:
#                     cleaned_data['grade'] = 'C'
#                     cleaned_data['grade_point'] = 2.0
#                 elif 35 <= score < 40:
#                     cleaned_data['grade'] = 'D'
#                     cleaned_data['grade_point'] = 1.0
#                 else:
#                     cleaned_data['grade'] = 'F'
#                     cleaned_data['grade_point'] = 0.0
#             except ValueError:
#                 self.add_error('score', 'Score must be a valid number')
#         return cleaned_data
