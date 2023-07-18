from django.urls import path
from . import views
app_name = 'hamim'
urlpatterns = [
    # Home page
    path('', views.index, name='index')
]