# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse, get_object_or_404
from .models import Task

from comments.models import Comment

from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.views.generic import UpdateView,CreateView
# Create your views here.
def task_list(request):

    context = {
        'tasks': Task.objects.all()
    }

    return render(request, 'tasks/tasks_list.html', context)


def task_detail(request, pk=None):

    task = get_object_or_404(Task, id=pk)

    if request.method == 'GET':
        task.usertask.add(request.user)
        task.save()
    if request.method == 'POST':
        if request.POST['type'] == 'comment':
            comment = Comment()
            comment.text = request.POST['comment']
            comment.author = request.user
            comment.task_id = pk
            comment.save()
            task.task_comments.add(comment)
            task.save()
        elif request.POST['type'] == 'close':
            task.is_finished = True
            task.save()
    context = {
        'task': task,
        'comments': Comment.objects.all().filter(task=task),

    }
    return render(request, 'tasks/tasks_detail.html', context)


class TaskEdit (UpdateView):
    model = Task
    fields = 'name',
    context_object_name = 'task'
    template_name = 'tasks/tasks_edit.html'


    def get_success_url(self):
        return reverse('task:task_detail', kwargs={'pk': self.object.pk})


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name','prescription','categories']

    def __init__(self,*args,**kwargs):
        super(TaskForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit','Сохранить'))




class TaskCreate(CreateView):
    form_class = TaskForm
    context_object_name = 'task'
    template_name = 'tasks/tasks_create.html'

    def form_valid(self, form):
        form.instance.auth = self.request.user
        return super(TaskCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('task:task_detail', kwargs={'pk': self.object.pk})
