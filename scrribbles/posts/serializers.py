from rest_framework import serializers
from .models import Post
from user.serializers import UserInformationSerializer


class CreatePostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ["title", "content", "tag", "image"]
	def create(self, validated_data):
		""" create post """
		print("--------")
		user = self.context['request'].user
		post = Post.objects.create(user=user, **validated_data)
		return post


class PostViewSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()
    user = UserInformationSerializer()

    class Meta:
        model = Post
        fields = "__all__"

    def get_tag(self, obj):
        return (obj.tag.name)


class PostInfoSearializer(serializers.ModelSerializer):
    user = UserInformationSerializer()
    tag = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["title", "content", "tag", "image", "featured", "user", "created_at"]
    # def get_user(self, obj):
    #     return f"{obj.user.get_full_name}"
    #
    #
    def get_tag(self, obj):
        return (obj.tag.name)
