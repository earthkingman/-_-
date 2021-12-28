from django.urls import path
from transaction.views import DepositView
urlpatterns = [
    path('/deposit', DepositView.as_view()),
    # path('/withdraw', Transaction.as_view()),
]