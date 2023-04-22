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
    path('cleaning/getDatasetCols',views.getDatasetCols,name='getDatasetCols'),
    path('merge/',views.dataMerge,name='dataMerge'),
    path('monitoring/', views.modelMonitoring, name='modelMonitoring'),
    path('retraining/', views.modelReTraining, name='modelReTraining'),
    path('errorAnalysis/', views.errorAnalysis, name='errorAnalysis'),
    path('useCases/', views.useCases, name='useCases'),
    path('errorAnalysis/upload', views.upload,name='upload'),
    path('cleaning/upload',views.upload,name='upload'),
    path('create/upload',views.upload,name='upload'),
    path('retrain/upload',views.upload,name='upload'),
    path('errorAnalysis/getDataset', views.getDataset,name='getDataset'),
    path('errorAnalysis/getPKL',views.getPKL,name='getPKL'),
    path('cleaning/getDataset',views.getDataset,name='getDataset'),
    path('listfiles',views.listfiles,name='listfiles'),
    path('getfile',views.getfile,name='getfile'),
    path('merge/getDataset',views.getDataset,name='getDataset'),
    path('merge/upload',views.upload,name='upload'),
    path('merge/getDatasetCols',views.getDatasetCols,name='getDatasetCols'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
