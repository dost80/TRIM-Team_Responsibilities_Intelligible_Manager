from django import forms
from .models import Team, TeamMember, Task, PRIORITIES, DAYS, STATUSES, FREQUENCIES
from django.core.validators import validate_email, URLValidator


DAYS = (
    (1, 'middle month'),
    (2, 'D-5'),
    (3, 'D-4'),
    (4, 'D-3'),
    (5, 'D-2'),
    (6, 'D-1'),
    (7, 'D1'),
    (8, 'D2'),
    (9, 'D3'),
    (10, 'D4'),
    (11, 'D5'),
)


PRIORITIES = (
    (1, 'high'),
    (2, 'middle'),
    (3, 'low'),
)


FREQUENCIES = (
    (1, 'monthly'),
    (2, 'quarterly'),
    (3, 'yearly'),
    (4, 'ad hoc'),
)


STATUSES = (
    (1, 'not started'),
    (2, 'in progress'),
    (3, 'completed'),
    (4, 'approved'),
)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', strip=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class AddUserForm(forms.Form):
    login = forms.CharField(label='Login', strip=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_check = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='First name', strip=True)
    last_name = forms.CharField(label='Last name', strip=True)
    email = forms.EmailField(label="Email")


class TaskForm(forms.Form):
    name = forms.CharField(label='Task')
    description = forms.CharField(label='Description')
    priority = forms.ChoiceField(label='Priority', choices=PRIORITIES)
    start_date = forms.DateTimeField(label='Start date')
    due = forms.ChoiceField(label='Due', choices=DAYS)
    frequency = forms.ChoiceField(label='Frequency', choices=FREQUENCIES)
    department = forms.CharField(label='Department')
    responsible = forms.CharField(label='Responsible')
    backup = forms.CharField(label='Backup')
    approver = forms.CharField(label='Approver')
    status = forms.ChoiceField(label='Status', choices=STATUSES)
    end_date = forms.DateTimeField(label='End date')


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'end_date']


class Search(forms.Form):
    position = forms.CharField(label='Position', max_length=64)
    # user = forms.CharField(label='User', max_length=64)
