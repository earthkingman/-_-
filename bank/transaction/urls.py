from django.urls import path
from transaction.views import DepositView, WithdrawView, SeedView, ListView, ListOffSetView
urlpatterns = [
    path('/deposit', DepositView.as_view()),
    path('/withdraw', WithdrawView.as_view()),
    path('/list', ListView.as_view()),
    path('/listoffset', ListOffSetView.as_view()),
    path('/seed', SeedView.as_view()),
]
