from django.urls import path

from . import views

urlpatterns = [
    path('', views.leaders_list, name='leaders_list'),
]
