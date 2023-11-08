"""
URL configuration for tp_web_askme_2023 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from ask_me import views

urlpatterns = [
    path('',                                            views.index,    name='index'),
    path('page/<int:page>',                             views.index,    name='index_page'),
    path('question/<int:question_id>',                  views.question, name='question'),
    path('question/<int:question_id>/page/<int:page>',  views.question, name='question_page'),
    path('tag/<str:tag_name>',                          views.tag,      name='tag'),
    path('tag/<str:tag_name>/page/<int:page>',          views.tag,      name='tag_page'),
    path('ask',                                         views.ask,      name='ask'),
    path('login',                                       views.login,    name='login'),
    path('logout',                                      views.logout,   name='logout'),
    path('register',                                    views.register, name='register'),
    path('settings',                                    views.settings, name='settings'),
    path('admin/', admin.site.urls),
]
