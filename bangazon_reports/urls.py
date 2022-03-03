from django.urls import path
from .views import CompletedOrderList
from .views import IncompleteOrderList
from .views import ExpensiveProductsList
from .views import InexpensiveProductsList
from .views import FaveStoreByCustomerList
urlpatterns = [
    path('completedorders', CompletedOrderList.as_view()),
    path('incompleteorders', IncompleteOrderList.as_view()),
    path('expensiveproducts', ExpensiveProductsList.as_view()),
    path('inexpensiveproducts', InexpensiveProductsList.as_view()),
    path('favestores', FaveStoreByCustomerList.as_view()),
]