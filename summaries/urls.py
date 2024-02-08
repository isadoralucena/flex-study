from django.urls import path
from . import views

urlpatterns = [
    path('create_summary/', views.create_summary, name='create_summary'),
    path('summary/<int:id>', views.summary, name='summary'),
]