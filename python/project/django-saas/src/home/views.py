from django.http import HttpResponse
from django.shortcuts import render

from visits.models import PageVisit


def home_page_view(request, *args, **kwargs):
    page_qs = PageVisit.objects.filter(path=request.path)
    html_context = {
        "text": "Hello World!",
        "page_visit_count": page_qs.count(),
    }
    html_template = "home.html"
    PageVisit.objects.create(path=request.path)

    return render(request, html_template, html_context)
