from django.urls import path
from . import views
urlpatterns = [
    path('/<int:id>', views.detail, name = 'detail'),
    path('/list', views.list, name = 'list')
]  
