from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.create_user_view, name='create'),
]