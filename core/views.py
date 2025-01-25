from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import WasteImage
from .forms import WasteImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def home(request):
    return render(request, 'index.html', {'user': request.user})

@login_required
def scan(request):
    return render(request, 'scan.html')

def contact(request):
    return render(request, 'contact.html')

@login_required
def complain(request):
    return render(request, 'complain.html')



class WasteImageListView(ListView):
    model = WasteImage
    template_name = 'waste_list.html'
    context_object_name = 'images'

class WasteImageDetailView(DetailView):
    model = WasteImage
    template_name = 'waste_detail.html'

class WasteImageUploadView(CreateView):
    model = WasteImage
    form_class = WasteImageForm
    template_name = 'waste_upload.html'
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Add your image processing logic here
        return response

