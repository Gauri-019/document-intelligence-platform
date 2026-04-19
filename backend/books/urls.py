from django.urls import path
from .views import list_books, book_detail, ask_question, recommend_books

urlpatterns = [
    path('books/', list_books),
    path('books/<int:pk>/', book_detail),
    path('books/<int:pk>/recommend/', recommend_books),
    path('ask/', ask_question),
]