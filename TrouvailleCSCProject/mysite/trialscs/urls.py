from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views_trials
'''
urlpatterns = [
    path('index', views.index, name='index'),
    path('travel_information',views.travel_information,name='travel_information'),
    path('verification', views.verification, name='verification'),
    path('home',views.home,name='home'),
    path('validate',views.validate,name='validate'),
    path('validate/results',views.results,name='results'),
    path('signup',views.results,name='results')
]
urlpatterns += staticfiles_urlpatterns()
'''

urlpatterns = [
    path('home', views_trials.home, name='home'),
    path('login',views_trials.login, name='login'),
    path('signup',views_trials.signup,name='signup'),
    path('signup/verification',views_trials.verification,name='verification'),
    path('signup/verification/auth',views_trials.auth,name='auth'),
    path('userdashboard',views_trials.userdashboard,name='userdashboard'),
    path('userdashboard/flights',views_trials.flights1,name='flights1'),
    path('userdashboard/flights/results',views_trials.flightsresults,name='flightsresults'),
    path('userdashboard/flights/results/choice',views_trials.flightchoice,name='flightchoice'),
    path('userdashboard/flights/results/choice/payment',views_trials.flightspayment,name='flightspayment'),
    path('userdashboard/flights/results/choice/payment/confirmation',views_trials.flightscon,name='flightscon'),
    path('ourteam',views_trials.ourteam,name='ourteam'),
    path('repa',views_trials.repa,name='repa'),
    path('twu',views_trials.twu,name='twu')


]
urlpatterns += staticfiles_urlpatterns()