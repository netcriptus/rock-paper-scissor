"""rock_paper_scissors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers

from player import views

router = routers.DefaultRouter()
router.register(r"players", views.PlayerViewSet)
router.register(r"matches", views.MatchViewSet)
router.register(r"scores", views.ScoreViewSet, basename="score")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
