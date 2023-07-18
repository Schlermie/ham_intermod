from django.shortcuts import render

# Create your views here.
def index(request):
    """ The home page for HamIM """
    return render(request, 'hamim/index.html')