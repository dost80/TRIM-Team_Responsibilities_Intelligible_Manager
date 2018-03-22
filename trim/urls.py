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
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin

from trim_app.views import MainView, TaskListView, AddUserView, UserLoginView, UserLogoutView,\
    TaskCreate, TaskDetailsView, UpdateTask, DeleteTask, TeamMemberView, AddTeamMemberView, TeamView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', MainView.as_view(), name="main"),
    url(r'^task_list$', TaskListView.as_view(), name="task-list"),
    url(r'^add_user$', AddUserView.as_view(), name="add-user"),
    url(r'^login$', UserLoginView.as_view(), name="login"),
    url(r'^logout$', UserLogoutView.as_view(), name="logout"),
    url(r'^create_task$', TaskCreate.as_view(), name="create-task"),
    url(r'^task_details/(?P<task_id>(\d)+)', TaskDetailsView.as_view(), name="task-details"),
    url(r'^update_task/(?P<pk>(\d)+)$', UpdateTask.as_view(), name="update-task"),
    url(r'^delete_task/(?P<pk>(\d)+)$', DeleteTask.as_view(), name="delete-task"),
    url(r'^team_member/(?P<teammember_id>(\d)+)', TeamMemberView.as_view(), name="team-member"),
    url(r'^add_team_member$', AddTeamMemberView.as_view(), name="add-team-member"),
    url(r'^team/(?P<id>(\d)+)', TeamView.as_view(), name="team"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)