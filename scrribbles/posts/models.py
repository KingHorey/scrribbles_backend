from django.db import models

from django.utils import timezone
from django.utils.text import slugify

from uuid import uuid4



class Tag(models.Model):
	id = models.UUIDField(default=uuid4, primary_key=True)
	name = models.CharField(max_length=15, null=False)
	slug = models.SlugField(null=False, blank=True)

	class Meta:
		verbose_name = 'tag'
		verbose_name_plural = 'tags'

	def save(self, *args, **kwargs):
		if not self.slug:
			slug = slugify(self.name)
			self.slug = slug
			super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.name}"


# Create your models here.
class Post(models.Model):
	id = models.UUIDField(default=uuid4, primary_key=True)
	title = models.CharField(max_length=256, null=False, blank=False)
	content = models.TextField()
	slug = models.SlugField(null=False, max_length=100)
	image = models.CharField(max_length=512, null=False, blank=True) # use cloudinary to get image link
	user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="posts")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(default=timezone.now)
	featured = models.BooleanField(blank=True, default=False, null=False)
	tag = models.ForeignKey(Tag, related_name="posts", on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		""" override the save method """
		if not self.slug:
			text = slugify(self.title)
			self.slug = text
		super().save(*args, **kwargs)

	class Meta:
		verbose_name = "post"
		verbose_name_plural = "posts"

	def __str__(self):
		""" str repr """
		return f"{self.title} by {self.user.get_full_name}"
