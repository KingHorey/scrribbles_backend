from django.urls import path

from .views import CreatePostView, PostInfoView, GetPost, UserPostView

urlpatterns = [
	path("post/create-post/", CreatePostView.as_view(), name="create-post"),
	path("post/", PostInfoView.as_view(), name="get post by query param"),
	path("post/get-post/<str:slug>/", GetPost.as_view(), name="get post, update and destroy"),
	path("post/my-post/", UserPostView.as_view(), name="user posts")
]

"""
path("post/recent-post/", RecentPostView.as_view(), name="recent posts"),
	path("post/featured-post/", FeaturedPostView.as_view(), name="featured posts"),
	path("post/<str: name>", PostByTagView.as_view(), name="post by tag")
"""
