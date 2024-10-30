from .models import User

from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .serializers import RegisterUserSerializer, UserInformationSerializer, CustomUserLoginSerializer

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from rest_framework import status

from rest_framework.permissions import IsAdminUser

from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.
class RegisterUserView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegisterUserSerializer

	def create(self, request, *args, **kwargs):
		""" handle user creation """
		user = self.get_serializer(data=request.data)
		try:
			user.is_valid(raise_exception=True)
			user.save()
			if user:
				# send mail
				return Response(user.data, status=status.HTTP_201_CREATED)
			else:
				return Response(user.error, status=status.HTTP_400_BAD_REQUEST)
		except ValidationError as e:
			return Response({
				"error": e.detail
				},
				status=status.HTTP_400_BAD_REQUEST
				)

class CustomLoginView(TokenObtainPairView):
	serializer_class = CustomUserLoginSerializer


class UserInformationView(RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	lookup_field = 'id'
	serializer_class = UserInformationSerializer

	def update(self, request, *args, **kwargs):
		user = self.request.user
		serializer = self.get_serializer(user, data=self.request.data, partial=True)
		try:
			serializer.is_valid(raise_exception=True)
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		except ValidationError as e:
			return Response({
						"error": e.detail
						},
						status=status.HTTP_400_BAD_REQUEST
						)


class AllUsersView(ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserInformationSerializer
	permission_classes = [IsAdminUser]