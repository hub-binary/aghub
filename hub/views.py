from django.shortcuts import render, redirect
from django.http import FileResponse
from .models import *
from filebrowser.base import FileObject



def events_view(request):
    template = 'public/index.html'
    context = {

    }
    return render(request, template, context)


def home_view(request):
    template = 'public/index.html'
    context = {

    }
    return render(request, template, context)


def sermons_view(request):
    results = Sermon.objects.all().order_by('-date_released')
    template = 'public/sermons.html'
    breadcrumbs = [
        ('Home', '/'),
        ('Sermons', request.path),
    ]
    context = {
        'sermons': results,
        'breadcrumbs': breadcrumbs
    }
    return render(request, template, context)


def contact_view(request):
    template = 'public/sermons.html'
    context = {

    }
    return render(request, template, context)


def weekly_schedule_view(request):
    template = 'public/week.html'
    context = {

    }
    return render(request, template, context)


def sermon_download_view(request, slug):
    sermon = Sermon.objects.get(url_title=slug)
    file_path = sermon.file_object.path_full
    

    # Creating a FileObject to get the file's content type
    file_name = sermon.file_object.name.split('/')[-1]  # Get the file name
    file_object = FileObject(file_path)
    content_type = file_object.filetype

    if request.method == 'GET':
        if request.GET.get('download', None):
            pass
        else:
            breadcrumbs = [
                ('Home', '/'),
                ('Sermons', '/sermons/'),
                (f'{sermon.sermon_title}', request.path),
            ]
            context = {
                'breadcrumbs': breadcrumbs,
                'sermon': sermon,
                'file_path': file_path,
            }
            return render(request, 'public/sermon-detail.html', context)

    # Set the appropriate response headers for the file download
    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{sermon.sermon_title}.mp3"'

    return response

