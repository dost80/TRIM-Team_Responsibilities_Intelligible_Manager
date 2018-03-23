from django import forms
from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy

from .models import Team, TeamMember, Task
from .forms import AddUserForm, LoginForm


class MainView(View):
    def get(self, request):
        task_list = Task.objects.filter(end_date=None).order_by('due')
        teammembers_list = TeamMember.objects.all()
        teams = Team.objects.all()
        ctx= {
            'task_list': task_list,
            'teammembers_list': teammembers_list,
            'teams': teams
        }
        if not request.user.is_authenticated:
            return redirect('login')
        return render(
            request,
            template_name='main.html',
            context=ctx
        )


class TaskListView(View):
    def get(self, request):
        task_list = Task.objects.all().order_by('due')
        ctx= {
            'task_list': task_list,
        }
        if not request.user.is_authenticated:
            return redirect('login')
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
                return redirect(reverse('main'))
            messages.success(request, "Wrong username or password, try again or contact an administrator.")
            return redirect(reverse('login'))
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


class TaskDetailsView(View):
    def get(self, request, task_id):
        task = Task.objects.get(id=task_id)
        ctx = {
            "task": task
        }
        return render(request, "task_details.html", ctx)


class TaskCreate(CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy('task-list')


class UpdateTask(UpdateView):

    model = Task
    # fields = "__all__"
    fields = ['status', 'end_date']
    success_url = reverse_lazy('task-list')


class DeleteTask(PermissionRequiredMixin, DeleteView):

    permission_required = 'trim_app.delete_task'
    raise_exception = True

    model = Task
    fields = "__all__"
    success_url = reverse_lazy('task-list')


class TeamMemberView(View):

    def get(self, request, teammember_id):
        team_member = TeamMember.objects.get(id=teammember_id)
        tasks_responsible = Task.objects.filter(responsible_id=teammember_id).order_by('due')
        tasks_approver = Task.objects.filter(approver_id=teammember_id).order_by('due')
        ctx = {
            "team_member": team_member,
            "tasks_responsible": tasks_responsible,
            "tasks_approver": tasks_approver,
        }
        return render(request, "team_member.html", ctx)


class AddTeamMemberView(PermissionRequiredMixin, CreateView):

    permission_required = 'trim_app.add_teammember'
    raise_exception = True

    model = TeamMember
    fields = "__all__"
    success_url = reverse_lazy('main')


class TeamView(View):

    def get(self, request, id):
        team = Team.objects.get(id=id)
        team_members = TeamMember.objects.filter(team_id=id)
        tasks = Task.objects.filter(department_id=id).order_by('due')
        ctx = {
            "team": team,
            "team_members": team_members,
            "tasks": tasks
        }
        return render(request, "team.html", ctx)


class UpdateApproval(PermissionRequiredMixin, UpdateView):

    permission_required = 'trim_app.change_task'
    raise_exception = True

    model = Task
    fields = ['approval', 'approval_date']
    success_url = reverse_lazy('task-list')


class UpdatePerson(PermissionRequiredMixin, UpdateView):

    permission_required = 'trim_app.change_task'
    raise_exception = True

    model = Task
    fields = ['responsible', 'backup', 'approver']
    success_url = reverse_lazy('task-list')
