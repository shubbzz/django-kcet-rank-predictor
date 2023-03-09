"""shubbhum URL Configuration

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',include('users.urls')),
    path('home',include('users.urls')),
    path('admin', admin.site.urls),
    path('cutoff',include('users.urls')),
    path('displaycutoff',include('users.urls')),
    path('predcollege',include('users.urls')),
    path('dispredcollege',include('users.urls')),
    path('predcourse',include('users.urls')),
    path('dispredcourse',include('users.urls')),
    path('kct',include('users.urls')),
    path('diskct',include('users.urls')),
    path('rank',include('users.urls')),
    path('disrank',include('users.urls')),

]
