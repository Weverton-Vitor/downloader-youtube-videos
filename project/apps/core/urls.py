from django.urls import path
from project.urls import path
from project.apps.core import views

app_name = 'core'

urlpatterns = [
    path('', views.YoutubeForm.as_view(), name='index')
]