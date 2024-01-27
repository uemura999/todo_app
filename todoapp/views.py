from typing import Any
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)

        searchInputText = self.request.GET.get("search") or ""
        if searchInputText:
            context['tasks'] = context['tasks'].filter(title__startswith=searchInputText) #__icontains

        context['search'] = searchInputText
        print(context)

        return context
        
    

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'task_create.html'
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('list')
    template_name = 'task_update.html'

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('list')
    template_name = 'task_delete.html'
    fields = '__all__'

class TaskListLogin(LoginView):
    fields = '__all__'
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('list')
    
class RegisterTodoApp(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('list')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
    


    
