# projects/urls.py
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "projects"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^projects/(?P<pk>\d+)$', views.projects, name='projects'),
    url(r'^search/$', views.get_data, name='search'),
    url(r'^search/results/(?P<data_pk>[\w-]+)/$', views.show_results, name='search_results'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)