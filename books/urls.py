from django.urls import path

from copies.views import CopyView
from .views import BookView, FollowView


urlpatterns = [
    path("books/", BookView.as_view()),
    path("book/<str:book_id>/copy/", CopyView.as_view()),
    path("book/<str:book_id>/follow/", FollowView.as_view()),
]
