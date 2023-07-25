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
            uploaded_file = request.FILES['file'].read().decode('utf-8')
            # Analyze the frequencies in the CSV file for intermod and display
            # the analysis results
            analysis_results = analyze(uploaded_file)
            # print(analysis_results)
            context = {
                'analysis_results': analysis_results
            }
            return render(request, 'hamim/upload_success.html', context)
    else:
        form = UploadFileForm()
    return render(request, 'hamim/index.html', {'form': form})