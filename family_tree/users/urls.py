from django.urls import path

from views import UserCreate, UserProfileDetail, UserProfileUpdate

app_name = 'users'

urlpatterns = [
    path('edit/', UserProfileUpdate.as_view(), name='profile_edit'),
    path('<str:username>/', UserProfileDetail.as_view(), name='profile'),
]