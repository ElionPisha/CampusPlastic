from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('materials/<int:page>/', views.material_list),
    path('material/<path:material_id>/', views.get_material_data)
]