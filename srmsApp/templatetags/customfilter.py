from atexit import register
from django import template
from cryptography.fernet import Fernet
from django.conf import settings


register = template.Library()

@register.filter
def replaceBlank(value,stringVal = ""):
    value = str(value).replace(stringVal, '')
    return value

@register.filter
def encryptdata(value):
    fernet = Fernet(settings.ID_ENCRYPTION_KEY)
    value = fernet.encrypt(str(value).encode())
    return value


@register.filter
def calculate_grade(score):
    if score >= 70:
        return 'A'
    elif 60 <= score <= 69: 
        return 'B+'
    elif 50 <= score <= 59: 
        return 'B'
    elif 40 <= score <= 49: 
        return 'C'
    elif 35 <= score <= 39: 
        return 'D'
    else: 
        return 'F'
        

@register.filter
def calculate_grade_point(score):
    if score >= 70:
        return 5.0
    elif 60 <= score <= 69: 
        return 4.0
    elif 50 <= score <= 59: 
        return 3.0
    elif 40 <= score <= 49: 
        return 2.0
    elif 35 <= score <= 39: 
        return 1.0
    else: 
        return 0