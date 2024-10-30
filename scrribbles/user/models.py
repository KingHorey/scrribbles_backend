from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser, PermissionsMixin
from django.utils import timezone


# other installed packages


""" other imports """
from uuid import uuid4
# Create your models here.

class CustomUser(UserManager):
	""" custom uer manager """
	def _prefill(self, email=None, password=None, **fields):
		if email is None:
			raise ValueError("An email needs to be provided")
		user = self.model(email=email, **fields)
		if password is None:
			user.set_unusable_password()
		else:
			user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **kwargs):
		""" creates an instance of a user """
		kwargs.setdefault('is_admin', False)
		kwargs.setdefault('is_staff', False)
		kwargs.setdefault('is_active', True)
		kwargs.setdefault('is_superuser', False)
		user = self._prefill(email=email, password=password, **kwargs)
		return user

	def create_superuser(self, email, password=None, **kwargs):
		""" creates an instance of a super user """
		kwargs.setdefault('is_admin', True)
		kwargs.setdefault('is_staff', True)
		kwargs.setdefault('is_active', True)
		kwargs.setdefault('is_superuser', True)
		user = self._prefill(email=email, password=password, **kwargs)
		return user


class User(AbstractUser, PermissionsMixin):
	id = models.UUIDField(primary_key=True, null=False, default=uuid4)
	first_name = models.CharField(max_length=15, null=False)
	last_name = models.CharField(max_length=15, null=False)
	email = models.EmailField(unique=True)
	profile_image = models.CharField(max_length=256, default="https://res.cloudinary.com/db2agmwon/image/upload/v1722207114/profile-default.256x256_gdbltu.png")
	username = None
	facebook = models.URLField(null=True, blank=True)
	x = models.URLField(null=True, blank=True)
	linked_in = models.URLField(null=True, blank=True)
	date_joined = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	@property
	def get_full_name(self):
		return f"{self.first_name} {self.last_name}"

	def __str__(self):
		return f"{self.get_full_name} with email: {self.email}"


	class Meta:
		verbose_name = 'user'
		verbose_name_plural = 'users'

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ['first_name', 'last_name']

	objects = CustomUser()
