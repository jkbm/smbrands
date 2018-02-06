
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from operator import itemgetter
import time

from django.shortcuts import render
from .models import Project, User, Twitter_data,  Dataset
from .forms import *


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.views import View


from .data import *
from .tasks import temp_task




# Create your views here.
def index(request):
    """
    Home page
    """


    return render(request, 'projects/index.html')

def projects(request):

    projects = Project.objects.all()

    if request.method == "POST":
        form = NewProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            project.save()
            if 'create' in request.POST:
                messages.info(request, 'Project created.')
                return redirect('projects:projects')
    else:
        form = NewProjectForm()

    return render(request, 'projects/projects.html', {'form': form, 'projects': projects})

def show_results(request, data_pk):
    data = Dataset.objects.get(pk=data_pk)
    texts = []
    
    try:
        dataj = json.load(open('projects/twitter/files/{0}.json'.format(data.filename), 'r'))
        statuses = dataj['statuses']

        for s in statuses:
            dset = [s['text'],s['favorite_count'], s['user']['screen_name'], s['created_at']]
            texts.append(dset)
        
        texts = sorted(texts, key=itemgetter(1), reverse=True)
    except Exception as e:
        print(e)
        json.loads(request.POST.get('DATA_NOT_RECIEVED_YETs', '{}'))



    return render(request, 'projects/results.html',{'texts': texts})

def get_data(request):
    if request.method == 'POST': # If the form has been submitted...
        form = GetDataForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            project = Project.objects.filter(name="temp")
            filename = form.cleaned_data['query'] + "_" + datetime.datetime.now().strftime("%d%m%Y_%H%M")
            result_type = form.cleaned_data['result_type']

            if form.cleaned_data['number'] > 0:
                number = form.cleaned_data['number']
            else:
                number = 150


            created_file = open('projects/twitter/files/{0}.json'.format(filename), 'w+')
            ds = Dataset.objects.create(project=project[0], filename=filename)
            
            
            query = form.cleaned_data['query']
            temp_task.delay(query, number, filename, result_type)
            #twitter_stream(query, 5, 10)

            print(form.cleaned_data['query'])

            time.sleep(10)

            return redirect('projects:search_results', data_pk=ds.pk) # Redirect after POST
    else:
        form = GetDataForm() # An unbound form

    return render(request, 'projects/get_data.html', {
        'form': form,
    })



