from django.shortcuts import render
from django.shortcuts import HttpResponse

from students.models import Student
from django.views import View

"""
def show_students(request):
    students = Student.objects.all()

    result = ""
    for s in students:
        result += s.name + "<br>"
    
    return HttpResponse(result)
"""

class ShowStudentsView(View):
    def get(request, *args, **kwargs):
        students = Student.objects.all()

        result = ""
        for s in students:
            result += s.name + "<br>"
        
        return HttpResponse(result)
