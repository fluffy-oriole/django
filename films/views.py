from django.views.generic import TemplateView
from django.http import HttpResponse
from films.models import Film
from typing import Any


class ShowFilmsView(TemplateView):
    template_name = "films/show_films.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["films"] = Film.objects.all()

        return context