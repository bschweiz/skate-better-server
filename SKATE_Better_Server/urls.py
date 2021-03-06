"""SKATE_Better_Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from skatebetterapi.views import register_user, login_user
from skatebetterapi.views import Skaters, Opponents, Tricks, Games, GameTricks

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'profile', Skaters, 'profile')
router.register(r'opponent', Opponents, 'opponent')
router.register(r'tricks', Tricks, 'trick')
router.register(r'gametricks', GameTricks, 'gametricks')
router.register(r'game', Games, 'game')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]