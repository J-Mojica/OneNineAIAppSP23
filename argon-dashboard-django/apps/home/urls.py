# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('create/', views.createModel, name='createModel'),
    path('cleaning/', views.dataCleaning, name='dataCleaning'),
    path('monitoring/', views.modelMonitoring, name='modelMonitoring'),
    path('retraining/', views.modelReTraining, name='modelReTraining'),
    path('useCases/', views.useCases, name='useCases'),
    path('cleaning/upload',views.upload,name='upload'),
    #path('cleaning/impute',views.impute,name='impute'),
    #path('cleaning/dropFeature',views.dropFeature,name='dropFeature'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
