from django.urls import path

from . import views

app_name='polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('/<response_id>/detail', views.detail, name='detail'),
    path('/<response_id>/result', views.result, name='result'),
    path('/<response_id>/vote', views.vote, name='votes'),
]