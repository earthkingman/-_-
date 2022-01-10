from django.urls import path
from transaction.views import DepositView, WithdrawView, ListView
urlpatterns = [
    path('deposit', DepositView.as_view()),
    path('withdraw', WithdrawView.as_view()),
    path('list', ListView.as_view()),
]
