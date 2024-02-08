from django.urls import path
from . import views

urlpatterns = [
    path('create_flashcard/', views.create_flashcard, name="create_flashcard"),
    path('delete_flashcard/<int:id>', views.delete_flashcard, name="delete_flashcard"),
    path('create_challenge/', views.create_challenge, name="create_challenge"),
    path('index_challenges/', views.index_challenges, name="index_challenges"),
    path('challenge/<int:id>/', views.challenge, name='challenge'),
    path('answer_flashcard/<int:id>/', views.answer_flashcard, name='answer_flashcard'),
    path('report/<int:id>/', views.report, name='report')
]