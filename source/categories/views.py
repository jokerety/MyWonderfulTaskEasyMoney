# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from .models import Category
from django import forms
from django.views.generic import UpdateView,CreateView
from django.urls import reverse_lazy
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
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
    if request.method == 'GET':
        form = CategoriesListForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data
            if data['sort']:
                categories = categories.order_by(data['sort'])
            if data['search']:
                categories = categories.filter(name__icontains=data['search'])

        context = {
            'categories': categories,
            'form': form,
        }
        return render(request, 'categories/categories_list.html', context)

    elif request.method == 'POST':
        return HttpResponseRedirect(reverse_lazy("core:login"))





class CategoryEdit (UpdateView):

    model = Category
    fields = 'name',
    context_object_name = 'category'
    template_name = 'categories/category_edit.html'


    def get_success_url(self):
        return reverse('categories:category_detail', kwargs={'pk': self.object.pk})


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']

    def __init__(self,*args,**kwargs):
        super(CategoryForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit','Сохранить'))


class CategoryCreate(CreateView):
    form_class = CategoryForm
    context_object_name = 'category'
    template_name = 'categories/category_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CategoryCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('categories:category_detail', kwargs={'pk': self.object.pk})


def category_detail(request, pk=None):

    category = get_object_or_404(Category, id=pk)

    context = {
        'category': category,
        'tasks': category.tasks.all().filter(is_finished=False)
    }
    return render(request, 'categories/category_detail.html', context)

