
from django.conf.urls import url
from django.contrib import admin

from task.views import task_list,task_detail, TaskCreate, TaskEdit

urlpatterns = [

    url(r'^$', task_list, name='task_list'),
    url(r'^(?P<pk>\d+)/detail/$', task_detail, name='task_detail'),
    url(r'^(?P<pk>\d+)/edit/$', TaskEdit.as_view(), name='task_edit'),
    url(r'^create/$', TaskCreate.as_view(), name='task_create'),
]
