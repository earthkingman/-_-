from django.urls import path
from account.views import AccountView
urlpatterns = [
    path('account', AccountView.as_view()),
]
