# projects/urls.py
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "projects"
urlpatterns = [
    url(r'^$', views.projects, name='home'),
    url(r'^projects/(?P<pk>[0-9a-f-]+)$', views.project, name='project_home'),
    url(r'^search/$', views.get_data, name='search'),
    url(r'^analysis/$', views.analyse, name='analysis'),
    url(r'^info/$', views.info, name='info'),
    url(r'^tasks/$', views.task_control, name='task_control'),
    url(r'^search/results/(?P<data_pk>[\w-]+)/$', views.show_results, name='search_results'),
    url(r'^analytics/words_(?P<dataset_pk>[\w-]+)/$$', views.analyze_data, name="analyze_words"),
    url(r'^api/projects/$', views.ProjectsCreateReadView.as_view(), name='projects_rest_api'),
    url(r'^api/projects/(?P<pk>[0-9a-f-]+)$', views.ProjectsReadUpdateDeleteView.as_view(), name='tournament_rest_api'),
    url(r'^temp/$', views.temp, name='temp')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)