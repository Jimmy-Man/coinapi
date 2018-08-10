#from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url


from . import views

urlpatterns = [
    url(r'^index/$',views.index,name='index'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^ajax/$',views.ajax,name='ajax')
    #url(r'^')
    #path('/index',views.index,name='index')
]