from django.urls import path

from . import views

urlpatterns = [
    # List/Create Application
    path('', views.ApplicationView.as_view()),
    # Retrieve/Update/Destroy Application
    path('<int:application_id>/', views.ApplicationDetailView.as_view()),
]
