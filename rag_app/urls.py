from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_document, name='upload_document'),
    path('query/', views.process_query, name='process_query'),
    path('history/', views.get_chat_history, name='get_chat_history'),
]