from django.http import HttpResponseRedirect
from django.shortcuts import render
from .im_analysis import analyze
from .forms import UploadFileForm

# Create your views here.
def index(request):
    """ The home page for HamIM """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(form.errors.as_data())
        if form.is_valid():
            # Check if the checkbox is checked for labeling the equations
            label_equations = 'labeleqns' in request.POST
            uploaded_file = request.FILES['file'].read().decode('utf-8')
            # Analyze the frequencies in the CSV file for intermod and display
            # the analysis results
            analysis_results = analyze(uploaded_file, label_equations)
            context = {
                'analysis_results': analysis_results
            }
            return render(request, 'hamim/upload_success.html', context)
    else:
        form = UploadFileForm()
    return render(request, 'hamim/index.html', {'form': form})

def about(request):
    """ HamIM version number and contact information """
    return render(request, 'hamim/about.html')

def makecsv(request):
    """ Teach the user how to make a CSV file """
    return render(request, 'hamim/makecsv.html')

def basics(request):
    """ Tell the user something about HamIM and how to use it """
    return render(request, 'hamim/basics.html')

def backups(request):
    """ Teach the user how to manage backup channels """
    return render(request, 'hamim/backups.html')
