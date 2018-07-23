
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from operator import itemgetter
from datetime import datetime
import time
import kombu.five

from django.shortcuts import render
from .models import Project, User, Twitter_data,  Dataset
from .forms import *
from .serializers import ProjectSerializer

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView 

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.views import View


from .data import *
from .tasks import temp_task, stream_task, premium_task
from celery.task.control import inspect, revoke

from .analytics import wordFreq




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
                return redirect('projects:home')
    else:
        form = NewProjectForm()

    return render(request, 'projects/projects.html', {'form': form, 'projects': projects})

def project(request, pk):

    project = Project.objects.get(pk=pk)

    datasets = Dataset.objects.filter(project=project).order_by('-pk')

    return render(request, 'projects/project.html', {'project': project, 'datasets': datasets})

def show_results(request, data_pk):
    data = Dataset.objects.get(pk=data_pk)
    project = data.project
    texts = []
    
    try:
        dataj = json.load(open('projects/twitter/files/{0}.json'.format(data.filename), 'r'))
        statuses = dataj['statuses']

        for s in statuses:
            dset = [s['text'],s['favorite_count'], s['user']['screen_name'], s['created_at'], s['text'].split('://')[-1]]
            texts.append(dset)
        
        texts = sorted(texts, key=itemgetter(1), reverse=True)
    except Exception as e:
        print(e)
        json.loads(request.POST.get('DATA_NOT_RECIEVED_YETs', '{}'))



    return render(request, 'projects/results.html',{'texts': texts, 'project': project, 'dataset': data})

def get_data(request):
    if request.method == 'POST': # If the form has been submitted...
        form = GetDataForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            project = Project.objects.filter(pk=form.cleaned_data['project'])
            filename = form.cleaned_data['query'] + "_" + datetime.now().strftime("%d%m%Y_%H%M")
            result_type = form.cleaned_data['result_type']

            if form.cleaned_data['number'] > 0:
                number = form.cleaned_data['number']
            else:
                number = 150


            created_file = open('projects/twitter/files/{0}.json'.format(filename), 'w+')
            ds = Dataset.objects.create(project=project[0], filename=filename, query=form.cleaned_data['query'])
            
            
            query = form.cleaned_data['query']
            print(form.cleaned_data['query'])
            if 'get_rest' in request.POST:
                temp_task.delay(query, number, filename, result_type)
                time.sleep(10)
                
            elif 'get_stream' in request.POST:
                stream_task.delay(query, number, filename, result_type)
            elif 'get_full' in request.POST:
                premium_task.delay(query, number, filename, result_type)
                if int(form.cleaned_data['number']) > 500:
                    time.sleep(10)
                elif int(form.cleaned_data['number']) > 5000:
                    time.sleep(15)
                else:
                    time.sleep(3)
            #twitter_stream(query, 5, 10)
        return redirect('projects:search_results', data_pk=ds.pk) # Redirect after POST
            

    else:
        form = GetDataForm() # An unbound form

    return render(request, 'projects/get_data.html', {
        'form': form,
    })

def analyze_data(request, dataset_pk):

    wordFreq(dataset_pk)

    jdata = json.load(open("projects/twitter/files/analysis_data.json",'r'))

    max_data = 0

    for it in jdata:
        if jdata[it] > max_data:
            max_data = jdata[it]

    return render(request, 'projects/chart_words.html', {'jdata': jdata, 'max_data': max_data })

def task_control(request):

    i = inspect()
    # Show the items that have an ETA or are scheduled for later processing
    scheduled = i.scheduled()

    scheduled = next (iter (scheduled.values()))
    # Show tasks that are currently active.
    active = i.active()
    active = next (iter (active.values()))

    for t in active:
        time_start = t['time_start']        
        t['time_start'] = datetime.fromtimestamp(time.time() - (kombu.five.monotonic() - time_start))

    # Show tasks that have been claimed by workers
    reserved = i.reserved()

    task_id = 0
    for i, e in request.POST.items():        
        if 'stop' in i:
            print(i, e)
            task_id = i

    if task_id in request.POST:
        task_id = task_id.split('stop')[-1]       
        print("Clossing task {0}".format(task_id))
        revoke(task_id, terminate=True)
        messages.info(request, 'Task stopped.')
        time.sleep(5)
        return render(request, 'projects/tasks.html', {
                    'scheduled': scheduled,
                    'active': active, 
                    'reserved': reserved})

    return render(request, 'projects/tasks.html', {
        'scheduled': scheduled,
        'active': active, 
        'reserved': reserved})

def analyse(request):

    return render(request, 'projects/analysis.html')

def temp(request):

    return render(request, 'projects/temp.html')


""" API VIEWS BELOW """

class ProjectsCreateReadView(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'name'

class ProjectsReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'pk'