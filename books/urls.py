from django.urls import path

from copies.views import CopyView
from .views import BookView


urlpatterns = [
    path("books/", BookView.as_view()),
    path("book/<str:book_id>/copy", CopyView.as_view()),
]
