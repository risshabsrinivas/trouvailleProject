from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('home', views.index, name='index'),

]
urlpatterns += staticfiles_urlpatterns()
