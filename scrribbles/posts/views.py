from django.shortcuts import render
from django.db.models import Q

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response

from rest_framework.exceptions import PermissionDenied

from .serializers import CreatePostSerializer, PostViewSerializer, PostInfoSearializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from .models import Post, Tag

# Create your views here.

class CreatePostView(ListCreateAPIView):
	serializer_class = CreatePostSerializer
	permission_classes = [IsAuthenticated]
	queryset = Post.objects.all()

	# def perform_create(self, serializer):
	# 	serializer.save(user=self.request.user)

	def create(self, request, *args, **kwargs):
		# print(self.request.data)
		user = request.user
		request_copy = request.data.copy()
		tag = request_copy.pop("tag", [])
		tag_exists, created = Tag.objects.get_or_create(name=tag)
		request_copy['tag'] = tag_exists.id;
		serializer = self.get_serializer(data=request_copy)
		if serializer.is_valid(raise_exception=True):
		  serializer.save()
		  return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
		  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RecentPostView(ListAPIView)
# FeaturedPostView
# PostByTagView
#
class PostInfoView(ListAPIView):
    """ Get post by query """
    queryset = Post.objects.all()
    serializer_class = PostViewSerializer

    def get_queryset(self):
        """ get param """
        params = self.request.query_params
        filter = Q()
        if 'tag' in params:
            query_name = params.getlist('tag')
            print(query_name)
            for tag in query_name:
                filter |= Q(tag__name__icontains=tag)
        if 'featured' in params:
            filter = Q(featured=True)
        # for param in params:
        result = self.queryset.filter(filter).order_by('-created_at')
        print(result)
        return result


class GetPost(RetrieveUpdateDestroyAPIView):
    serializer_class = PostInfoSearializer
    lookup_field = "slug"

    def get_queryset(self, *args, **kwargs):
        key = self.kwargs.get('slug')
        queryset = Post.objects.filter(slug=key)
        return queryset

    # def update(self, request, *args, **kwargs):
    #     """ update the post information """
    #     serializer = self.get_serializer(data=request.data, partial=True)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPostView(ListAPIView):
    serializer_class = PostViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print(user)
        queryset = Post.objects.filter(user=user)
        print(queryset)
        return queryset
