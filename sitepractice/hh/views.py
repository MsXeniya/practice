from django.contrib.sites import requests
from django.shortcuts import render
from django.http import HttpResponse
# def index(request):
#     return HttpResponse("Страница приложения hh.")
#
# def categories(request, cat_id):
#     return HttpResponse(f"<h1>Раздел по категориям</h1><p>id: {cat_id}</p>")
#
# def categories_by_slug(request, cat_slug):
#     return HttpResponse(f"<h1>Раздел по категориям</h1><p>slug: {cat_slug}</p>")
#
# def page_not_found(request, exception):
#     return HttpResponseNotFound("<h1>Страница не найдена</h1>")


from django.shortcuts import render
from django.http import JsonResponse
from .parser import fetch_resume_data

def search_form(request):
    return render(request, 'hh/search_form.html')


def parse_resumes(request):
    name = request.GET.get('name', '')
    skills = request.GET.get('skills', '')
    job_title = request.GET.get('job_title', '')

    query = f"{name} {skills} {job_title}".strip()
    area = request.GET.get('area', 1)
    page_size = request.GET.get('page_size', 20)
    page = request.GET.get('page', 1)

    resumes = fetch_resume_data(query=query, area=area, page_size=page_size)
    return JsonResponse(resumes, safe=False)





