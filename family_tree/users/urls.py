from django.urls import path

from .views import UserProfileDetail, UserProfileLogout, UserProfileUpdate

app_name = 'users'

urlpatterns = [
    path('edit/', UserProfileUpdate.as_view(), name='profile_edit'),
    path('logout/', UserProfileLogout.as_view(), name='profile_logout'),
    path('<str:username>/', UserProfileDetail.as_view(), name='profile'),
]