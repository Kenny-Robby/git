from unittest import result
from django.db import models
from django.db.models import Sum
from django.utils import timezone


# Create your models here.
class Class(models.Model):
    level = models.CharField(max_length=250)
    course = models.CharField(max_length=250)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default = 1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.level + ' - ' + self.course)


#semester
class Semester(models.Model):
    semester_number = models.IntegerField(unique=True, default=1)  

#subject     
class Subject(models.Model):
    # semesterNo = models.ForeignKey(Semester, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=250, default='', blank=True)
    credit = models.IntegerField(default=0)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default = 1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    classI = models.ForeignKey(Class, on_delete= models.CASCADE)
    student_id = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250, blank= True, null=True)
    last_name = models.CharField(max_length=250)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=(('Male','Male'),('Female','Female')), default = 1)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default = 1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.student_id + " - " + self.first_name + " " + (str(self.middle_name + " " + self.last_name)  if self.middle_name != '' else self.last_name ))

    def get_name(self):
        return str(self.first_name + " " + (str(self.middle_name + " " + self.last_name)  if self.middle_name != '' else self.last_name ))

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.CharField(max_length=250,blank=True)
    gpa = models.FloatField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.semester} - {self.gpa}"
   

    def countSubjects(self):
        try:
            resultCount = Student_Subject_Result.objects.filter(result = self).count()
        except:
            resultCount = 0
        return resultCount

    def average(self):
        try:
            resultCount = Student_Subject_Result.objects.filter(result = self).count()
            results = Student_Subject_Result.objects.filter(result = self).aggregate(Sum('score'))['score__sum']
            if not results is None:
                average = results / resultCount
        except Exception as err:
            print(err)
            average = 0
        return average
    
    # # gpa
    def calculate_gpa(self):
        total_credits = 0
        total_grade_points = 0
        subjects_results = Student_Subject_Result.objects.filter(result=self)

        for subject_result in subjects_results:
            credit = subject_result.subject.credit
            grade_point = subject_result.grade_point
            total_credits += credit
            total_grade_points += grade_point * credit

        if total_credits > 0:
            gpa = total_grade_points / total_credits
            return round(gpa, 2)
        else:
            return 0.0
   



class Student_Subject_Result(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    grade = models.CharField(max_length=2, blank=True, null=True)
    grade_point = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.score >= 70:
            self.grade = 'A'
            self.grade_point = 5.0
        elif 60 <= self.score < 70:
            self.grade = 'B+'
            self.grade_point = 4.0
        elif 50 <= self.score < 60:
            self.grade = 'B'
            self.grade_point = 3.0
        elif 40 <= self.score < 50:
            self.grade = 'C'
            self.grade_point = 2.0
        elif 35 <= self.score < 40:
            self.grade = 'D'
            self.grade_point = 1.0
        else:
            self.grade = 'F'
            self.grade_point = 0.0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.result} - {self.subject} - Score: {self.score} - Grade: {self.grade} - Grade Point: {self.grade_point}"


      # gpa
    def calculate_gpa(self):
        total_credits = 0
        total_grade_points = 0
        subjects_results = Student_Subject_Result.objects.filter(result=self)

        for subject_result in subjects_results:
            credit = subject_result.subject.credit
            grade_point = subject_result.grade_point
            total_credits += credit
            total_grade_points += grade_point * credit

        if total_credits > 0:
            gpa = total_grade_points / total_credits
            return round(gpa, 2)
        else:
            return 0.0

