from django.urls import path
from .views import CompletedOrderList
from .views import IncompleteOrderList

urlpatterns = [
    path('completedorders', CompletedOrderList.as_view()),
    path('incompleteorders', IncompleteOrderList.as_view()),
]