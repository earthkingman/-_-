from django.urls import path
from transaction.views import DepositView, WithdrawView, SeedView
urlpatterns = [
    path('/deposit', DepositView.as_view()),
    path('/withdraw', WithdrawView.as_view()),
    path('/seed', SeedView.as_view()),
]