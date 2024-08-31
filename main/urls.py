from django.urls import path
from .views import main_page, SignupView, LoginView  # Assuming you have these views

urlpatterns = [
    path('', main_page, name='main_page'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]
