
from django.conf.urls import url, include
from django.contrib import admin

from categories.views import  categories_list, category_detail, CategoryEdit, CategoryCreate

urlpatterns = [

    url(r'^$', categories_list, name='categories_list'),
    url(r'^(?P<pk>\d+)/detail/$', category_detail, name='category_detail'),
    url(r'^(?P<pk>\d+)/edit/$', CategoryEdit.as_view(), name='category_edit'),
    url(r'^create/$', CategoryCreate.as_view(), name = 'category_create'),

]
