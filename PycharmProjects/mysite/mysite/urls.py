"""mysite URL Configuration

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
from django.urls import path
from django.conf.urls import url
from . import initViews
from .Views.ViewsSingleJq import singlejq
from .Views.ViewsAllJq import alljq
from .Views.ViewsKindJq import kindjq
urlpatterns = [
    url(r'^admin',admin.site.urls),
    url(r'^index$',initViews.index,name='index'),
    url(r'^singlejq$',singlejq,name='singlejq'),
    url(r'^kindjq$',kindjq,name='kindjq'),
    url(r'^alljq$',alljq,name='alljq'),
    #url(r'^index2$',views.index2,name='index2'),
    url(r'^indexall$',initViews.indexall,name='indexall'),
]
