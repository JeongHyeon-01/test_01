from django.urls import path, include
from users.views import SignUpView,SigninView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SigninView.as_view())
]
