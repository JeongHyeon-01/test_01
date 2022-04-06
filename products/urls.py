from django.urls import path
from .views import DetailView,ProductListView,SmartSearchView
urlpatterns = [
    path('',ProductListView.as_view()),
    path('/<int:product_id>', DetailView.as_view()),
    path('/smart',SmartSearchView.as_view())
]
