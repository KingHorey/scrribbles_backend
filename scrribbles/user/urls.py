from django.urls import path

from .views import RegisterUserView, UserInformationView, AllUsersView

urlpatterns = [
	path("user/auth/register/", RegisterUserView.as_view(), name="register user"),
	path("user/account/<str:id>/", UserInformationView.as_view(), name="user information"),
	path("user/all-users/", AllUsersView.as_view(), name="all users"),
]