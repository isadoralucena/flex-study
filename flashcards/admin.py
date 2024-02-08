from django.contrib import admin
from . models import Category, Flashcard, FlashcardChallenge, Challenge

admin.site.register(Category)
admin.site.register(Flashcard)
admin.site.register(FlashcardChallenge)
admin.site.register(Challenge)