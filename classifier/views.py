from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ImageUploadForm
from .models import Image
import zipfile36 as zipfile
from PIL import Image as pillow_image

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
    # required_zip.zipped_images.extractall()
    print(required_zip)
    zf = zipfile.ZipFile(required_zip.zipped_images)
    foldername = zf.filename[:-4]
    zf.extractall(path="media/" + foldername)
    filenames = zf.namelist()
    print(zf.filename)
    path = "media/" + foldername + "/"
    for filename in filenames:
        final_path = path + filename
        img = pillow_image.open(final_path)
        print(img.height, img.width)
        output_size = (350, 350)
        img = img.resize(output_size)
        print(img.height, img.width)
        img.save(final_path)
    # with zipfile.ZipFile(required_zip.zipped_images, 'r') as z:
    #     for f in z.namelist():
    #         images.update({f: base64.b64encode(z.read(f)), })
    context = {
        "foldername": foldername,
        "filenames": filenames
    }
    return render(request, 'classifier/home.html', context)
