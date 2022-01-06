from django.urls import path
from transaction.views import DepositView, WithdrawView, SeedView, ListView
urlpatterns = [
    path('deposit', DepositView.as_view()),
    path('withdraw', WithdrawView.as_view()),
    path('list', ListView.as_view()),
    path('seed', SeedView.as_view()),
]

# urls.py에서 url 경로와 view.py의 함수를 매핑해줄 때, 함수만 가능하기 때문에
#  Class를 view로 이용하는 경우에는 as_view()를 붙여줘야해요. 그래야 Django가 Class를 View로써 인식할 수 있답니다.
