from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

# Create your views here.
def index(request):
    """ The home page for HamIM """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(form.errors.as_data())
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_content = uploaded_file.read().decode('utf-8')
            # Do something with the file content
            # For example, print it:
            print(file_content)
            return render(request, 'hamim/upload_success.html')
    else:
        form = UploadFileForm()
    return render(request, 'hamim/index.html', {'form': form})