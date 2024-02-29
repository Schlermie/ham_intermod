from django.urls import path
from . import views
app_name = 'hamim'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # About page
    path('about/', views.about, name='about'),
    # HamIM version number and contact information
    path('basics/', views.basics, name='basics'),
    # How to Create a CSV page
    path('makecsv/', views.makecsv, name='makecsv'),
    # How to Manage Backup Channels page
    path('backups/', views.backups, name='backups')
]