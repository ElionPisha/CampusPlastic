from django.shortcuts import render
from WebScrapingUtils.web_scrapper_util import get_page, get_data_from_url


def index(request):
    return render(request, "index.html")


def material_list(request, page):
    list_of_links = get_page(page)
    return render(request, "index.html", context={"links": list_of_links})


def get_material_data(request, material_id):
    data = get_data_from_url(material_id)
    return render(request, "material_detail.html", context={"data": data})

