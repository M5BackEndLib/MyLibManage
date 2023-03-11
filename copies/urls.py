from django.urls import path
from .views import CopyLoanCreateAPIView, UserLoanListView, ReturnCopyView

urlpatterns = [
    path("loan/", UserLoanListView.as_view()),
    path("loan/<str:id>/", CopyLoanCreateAPIView.as_view()),
    path("return/<str:id>/", ReturnCopyView.as_view()),
]
