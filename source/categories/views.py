# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse, HttpResponse, get_object_or_404
from .models import Category
from django import forms
from django.views.generic import UpdateView,CreateView

# Create your views here.

class CategoriesListForm (forms.Form):

    sort = forms.ChoiceField(choices=(
        ('name', "Name asc"),
        ('-name', 'Name desc'),
        ('id', 'ID'),
    ), required= False)
    search = forms.CharField(required=False)


def categories_list(request):

    categories = Category.objects.all()

    form = CategoriesListForm(request.GET)
    if form.is_valid():
        data = form.cleaned_data
        if data['sort']:
            categories = categories.order_by(data['sort'])
        if data['search']:
            categories = categories.filter(name__icontains= data['search'])

    context = {
        'categories': categories,
        'form': form,
    }

    return render (request, 'categories/categories_list.html', context)


class CategoryEdit (UpdateView):

    model = Category
    fields = 'name',
    context_object_name = 'category'
    template_name = 'categories/category_edit.html'

    def get_queryset(self):
        queryset = super(CategoryEdit,self).get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse('categories:category_detail', kwargs={'pk': self.object.pk})


class CategoryCreate(CreateView):
    model = Category
    fields = 'name',
    context_object_name = 'category'
    template_name = 'categories/category_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CategoryCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('categories:category_detail', kwargs={'pk': self.object.pk})


def category_detail(request, pk=None):

    category =  get_object_or_404(Category, id=pk)

    context = {
        'category': category,
        'tasks': category.tasks.all().filter(is_archieve=False)
    }
    return render(request, 'categories/category_detail.html', context)

