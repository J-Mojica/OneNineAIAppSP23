from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='transform-home'),
    path('upload',views.upload,name='upload'),
    path('impute',views.impute,name='impute'),
    path('dropFeature',views.dropFeature,name='dropFeature')
]