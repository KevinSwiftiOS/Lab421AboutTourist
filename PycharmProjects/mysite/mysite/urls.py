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
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from . import initViews
from .Views.ViewsInnerScenic import InnerScenic
from .Views.ViewsCircularAnalysis import CircularAnalysis
from .Views.ViewsComparedAnalysis import ComparedAnalysis
from .Views.ViewsRecentState import RecentState
admin.autodiscover()
urlpatterns = [
    url(r'^admin',admin.site.urls),
    url(r'^$', initViews.homepage),
    url(r'^InnerScenic$',InnerScenic,name='InnerScenic'),
    url(r'^ComparedAnalysis$',ComparedAnalysis,name='ComparedAnalysis'),
    url(r'^CircularAnalysis$',CircularAnalysis,name='CircularAnalysis'),
    url(r'^RecentState$', RecentState, name='RecentState'),
    #url(r'^index2$',views.index2,name='index2'),
]
