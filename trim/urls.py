"""trim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from trim_app.views import TaskListView, AddUserView, UserLoginView, UserLogoutView, \
    AddTaskView, TaskCreate, UpdateTask, TeamMemberView, SearchView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TaskListView.as_view(), name="main"),
    url(r'^add_user$', AddUserView.as_view(), name="add-user"),
    url(r'^login$', UserLoginView.as_view(), name="login"),
    url(r'^logout$', UserLogoutView.as_view(), name="logout"),
    url(r'^add_task$', AddTaskView.as_view(), name="add-task"),
    url(r'^create_task$', TaskCreate.as_view(), name="create-task"),
    url(r'^update_task/(?P<pk>(\d)+)$', UpdateTask.as_view(), name="update-task"),
    url(r'^team_member/(?P<teammember_id>(\d)+)', TeamMemberView.as_view(), name="team-member"),
    url(r'^search$', SearchView.as_view(), name='search'),
]
