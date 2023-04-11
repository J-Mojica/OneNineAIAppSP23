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
    path('errorAnalysis/', views.errorAnalysis, name='errorAnalysis'),
    path('useCases/', views.useCases, name='useCases'),
    path('cleaning/upload',views.upload,name='upload'),
    path('create/upload',views.upload,name='upload'),
    path('retrain/upload',views.upload,name='upload'),
    path('cleaning/getDataset',views.getDataset,name='getDataset'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
