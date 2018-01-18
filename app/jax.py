# coding=utf-8

from django.conf.urls import url, include
from . import views, datatrans, mobile
from django.contrib import admin

urlpatterns = (
    url(r'^mobile.do$', mobile.safed, name='safed'),
)
