from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='transform-home'),
    path('upload',views.upload,name='upload')
]