from django.db import models

from uuid import uuid4
# Create your models here.

class NewsLetter(models.Model):
	id = models.UUIDField(default=uuid4, primary_key=True)
	email = models.EmailField(unique=True, null=False, blank=False)
	subscription_status = models.BooleanField(default=False)
	subscription_date = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.email
