from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView

"""
def show_students(request):
    students = Student.objects.all()

    result = ""
    for s in students:
        result += s.name + "<br>"
    
    return HttpResponse(result)


class ShowStudentsView(TemplateView):
    template_name = "students/show_students.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all()
        print("got_extra_data")

        return context
"""