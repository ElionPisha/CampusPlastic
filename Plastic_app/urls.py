from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('materials/<int:page>/', views.material_list),
    # Example: when we hit 'materials/2' we call the function material_list that is inside
    # views.py file, and pass the page as a parameter to the function
    path('material/<path:material_id>/', views.get_material_data)
]