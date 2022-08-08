from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.create_user_view, name='create'),
    path('token/', obtain_auth_token, name='token'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]