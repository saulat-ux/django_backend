from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView  # Import TokenRefreshView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT refresh view

    path('job-posts/', views.job_post_list_create, name='job_post_list_create'),  # List and create job posts
    path('job-posts/<int:pk>/', views.job_post_detail, name='job_post_detail'),   # Retrieve, update, and delete a job post
]
