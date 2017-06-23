'''
Created on 2017年6月17日

@author: huangxing
'''
from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', view=views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag')
]