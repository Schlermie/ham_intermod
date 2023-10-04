from django.urls import path
from . import views
app_name = 'hamim'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # About page
    path('about/', views.about, name='about'),
    # How to Create a CSV page
    path('makecsv/', views.makecsv, name='makecsv')
]