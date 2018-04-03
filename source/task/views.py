# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse, HttpResponse,get_object_or_404
from .models import Task
from django.views.generic import UpdateView,CreateView
# Create your views here.
def task_list(request):

    context = {
        'tasks': Task.objects.all()
    }

    return render(request, 'tasks/tasks_list.html', context)


def task_detail(request, pk=None):

    task =  get_object_or_404(Task, id=pk)

    context = {

        'task': task
    }
    return render(request, 'tasks/tasks_detail.html', context)

class TaskEdit (UpdateView):

    model = Task
    fields = 'name',
    context_object_name = 'task'
    template_name = 'tasks/tasks_edit.html'

    def get_queryset(self):
        queryset = super(TaskEdit, self).get_queryset()
        queryset = queryset.filter(auth=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse('task:task_detail', kwargs={'pk': self.object.pk})


class TaskCreate(CreateView):
    model = Task
    fields = 'name','categories'
    context_object_name = 'task'
    template_name = 'tasks/tasks_create.html'

    def form_valid(self, form):
        form.instance.auth = self.request.user
        return super(TaskCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('task:task_detail', kwargs={'pk': self.object.pk})
