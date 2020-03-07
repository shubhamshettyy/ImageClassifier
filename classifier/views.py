from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ImageUploadForm
from .models import Image
import zipfile36 as zipfile
import base64

# Create your views here.


def upload(request):
    if request.method == 'POST':
        i_form = ImageUploadForm(request.POST, request.FILES)
        if i_form.is_valid():
            i_form.save()
            messages.success(request, f'Your file has been uploaded!')
            return redirect('home')
    else:
        i_form = ImageUploadForm()
    context = {
        'i_form': i_form
    }
    return render(request, 'classifier/upload.html', context)


def home(request):
    images = {}
    required_zip = Image.objects.last()
    print(required_zip)
    zf = zipfile.ZipFile(required_zip.zipped_images)
    print(zf.namelist())
    with zipfile.ZipFile(required_zip.zipped_images, 'r') as z:
        for f in z.namelist():
            images.update({f: base64.b64encode(z.read(f)), })
    context = {
        "images": images,
    }
    return render(request, 'classifier/home.html', context)
