from django.urls import path
from .views import CopyLoanCreateAPIView, UserLoanListView, ReturnCopyView

urlpatterns = [
    path("loan/", UserLoanListView.as_view()),
    path("loan/<str:user_id>/copy/<str:copy_id>/", CopyLoanCreateAPIView.as_view()),
    path("return/<str:loan_id>/", ReturnCopyView.as_view()),
]
