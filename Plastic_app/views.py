from django.shortcuts import render
from WebScrapingUtils.web_scrapper_util import get_page, get_data_from_url
# Create your views here.


def index(request):
    return render(request, "index.html")


def material_list(request, page):
    # here we call the get_page function that we have imported and pass the page to make a
    # request to the website and get the list of data for that page
    list_of_links = get_page(page)
    # we return the data to the index.html page were we display the data
    return render(request, "index.html", context={"links": list_of_links})


def get_material_data(request, material_id):
    data = get_data_from_url(material_id)
    return render(request, "material_detail.html", context={"data": data})

