from django import forms
from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy

from .models import Team, TeamMember, Task
from .forms import AddUserForm, LoginForm, TaskListForm, AddTaskForm, EditTaskForm, Search


class TaskListView(View):
    def get(self, request):
        task_list = Task.objects.filter(end_date=None).order_by('due')
        # task_list = Task.objects.all().order_by('due')
        teammembers_list = TeamMember.objects.all()
        ctx= {
            'task_list': task_list,
            'teammembers_list': teammembers_list
        }
        return render(
            request,
            template_name='task_list.html',
            context=ctx
        )


class AddUserView(View):
    def get(self, request):
        form = AddUserForm()
        ctx = {
            'form': form
        }
        return render(
            request,
            template_name='add_user.html',
            context=ctx
        )

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            if User.objects.filter(username=login).exists():
                form.add_error('login', "Taki login jest już zajęty.")
            password = form.cleaned_data['password']
            password_check = form.cleaned_data['password_check']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            if password != password_check:
                form.add_error('password', "Hasła do siebie nie pasują.")
            if not form.errors:
                email = form.cleaned_data['email']
                User.objects.create_user(login, email, password,
                                         first_name=first_name,
                                         last_name=last_name)
                return HttpResponse("Udało sie założyć nowego użytkownika")
            ctx = {
                'form': form
            }
            return render(
                request,
                template_name='add_user.html',
                context=ctx
            )


class UserLoginView(View):
    def get(self, request):
        form = LoginForm()
        ctx = {
            'form': form
        }
        return render(
            request,
            template_name='login.html',
            context=ctx
        )

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Udało się zalogować")
                return redirect(reverse('main'))
            return HttpResponse("No nie koniecznie")
        ctx = {
            'form': form
        }
        return render(
            request,
            template_name='exercises/login.html',
            context=ctx
        )


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('main'))


class AddTaskView(View):
    def get(self, request):
        form = AddTaskForm()
        ctx = {
            'form': form
        }
        return render(
            request,
            template_name="task.html",
            context=ctx
        )

    def post(self, request):
        form = AddTaskForm(request.POST)
        ctx = {
            'form': form
        }
        if form.is_valid():
            form.save()
            return redirect(reverse('main'))
        return render(
            request,
            template_name="task.html",
            context=ctx
        )


class TaskCreate(CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy('main')


class UpdateTask(UpdateView):
    model = Task
    # fields = "__all__"
    fields = ['status', 'end_date']
    success_url = reverse_lazy('main')


class TeamMemberView(View):

    def get(self, request, teammember_id):
        team_member = TeamMember.objects.get(id=teammember_id)
        tasks_responsible = Task.objects.filter(responsible_id=teammember_id)
        tasks_approver = Task.objects.filter(approver_id=teammember_id)
        ctx = {
            "team_member": team_member,
            "tasks_responsible": tasks_responsible,
            "tasks_approver": tasks_approver,
        }
        return render(request, "team_member.html", ctx)


class SearchView(View):
    def get(self, request):
        form = Search()
        ctx = {
            'form': form
        }
        return render(request,
                      template_name="search.html",
                      context=ctx)

    def post(self, request):
        form = Search(request.POST)
        if form.is_valid():
            position = form.cleaned_data['position']
            user = form.cleaned_data['task']
            found_team_members = TeamMember.objects.filter(position__icontains=position)
            found_user = User.objects.filter(last_name__icontains=user)
            ctx = {
                "team_members": found_team_members
            }
            return render(request,
                          template_name="search_result.html",
                          context=ctx)
