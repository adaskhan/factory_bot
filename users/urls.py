from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_token_auth'),
]
