from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=32)
    team = models.ForeignKey(Team, related_name='team_member', on_delete=models.CASCADE)

    @property
    def name(self):
        first_name = self.user.first_name
        last_name = self.user.last_name
        return "{} {}".format(first_name, last_name)

    def __str__(self):
        return self.name


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


class Task(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(default=None, blank=True)
    priority = models.IntegerField(choices=PRIORITIES)
    start_date = models.DateTimeField(default=datetime.now, blank=True)
    due = models.IntegerField(choices=DAYS)
    frequency = models.IntegerField(choices=FREQUENCIES)
    department = models.ForeignKey(Team, related_name='task_team', on_delete=models.CASCADE)
    responsible = models.ForeignKey(TeamMember, related_name='task_person', on_delete=models.CASCADE)
    backup = models.ForeignKey(TeamMember, related_name='task_backup', on_delete=models.CASCADE, blank=True)
    approver = models.ForeignKey(TeamMember, related_name='task_approver', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUSES)
    end_date = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return self.name
