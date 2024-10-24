from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('ajax/load-municipios/', views.load_municipios, name = 'load_municipios')
]
