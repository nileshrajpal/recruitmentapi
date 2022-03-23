from django.urls import path

from . import views

urlpatterns = [
    # For Admin registration (is_admin=True)
    path('register/', views.UserRegisterView.as_view()),
    # For Admin/Candidate
    path('login/', views.UserLoginView.as_view()),
    # For Admin/Candidate
    path('logout/', views.UserLogoutView.as_view()),
]
