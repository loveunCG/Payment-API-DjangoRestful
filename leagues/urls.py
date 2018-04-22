"""leagues URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from league import views as league_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', league_view.league),
    path('accounts/', include('league.urls')),
    path('leagues/', league_view.league, name='leagues'),
    path('notification/', league_view.notification, name='notification'),
    path('ajax_save_leagues/', league_view.save_league, name = 'ajax_save_leagues'),
    path('ajax_get_league_userlist/', league_view.get_league_userlist, name = 'get_league_userlist'),
    path('ajax_delete_league/', league_view.delete_league, name = 'delete_league'),
    path('ajax_join_league/', league_view.join_league, name = 'join_league'),
    path('ajax_send_invite/', league_view.send_invitation, name = 'send_invitation'),
    path('ajax_get_leagues_table/', league_view.get_leagues_table, name = 'get_table_league'),
    path('accounts/', include('django.contrib.auth.urls')),
]
