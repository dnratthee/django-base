"""
URL configuration for base project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("thai/", include("thai.urls")),
    # path('', views.home, name='home') # from my_app import views
    # path('', Home.as_view(), name='home') # from other_app.views import Home
]
