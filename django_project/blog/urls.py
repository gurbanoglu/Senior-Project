from django.urls import path

# Holds the URLs for the "blog" application.

# Import all of the class-based views that were created in the blog -> views.py file.
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    ViewMenu
)

# Import the views.py module. The "." represents the current directory.
from . import views

# This is where URL routes can be appended to the web application.
urlpatterns = [
    # Since the first URL pattern is the home page, the first argument for path is an
    # empty string.
    # views.home references the "home" function that was created in views.py which
    # returns an http response.
    # The name of the home URL pattern is 'blog-home'.
    # path('', views.home, name='blog-home'),

    # Instead of using the home view, use the class-based called "PostListView".

    # The following is where the class-based view called "PostListView" is looking:
    # <application>/<model>_<view_type>.html
    # <blog>/<post>_<list>.html
    path('', PostListView.as_view(), name='blog-home'),
    # The following route has a variable "pk" which represents the primary
    # key of the post that is requested for viewing. "int:pk" tells django
    # that only integers are expected after 'post/'. Always end a route
    # with a trailing slash ("/"). "PostDetailView" will handle the route.
    # By including the "pk" variable in the URL, the value from the URL is
    # grabbed and utilised it in the view function which is the class-based
    # view called "PostDetailView". E.g. localhost:8000/post/1/
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # The following is a URL pattern for creating a new post:
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    # If someone wanted to update a post with an id of 6, they would enter
    # in the following in the URL: localhost:8000/post/6/update/
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),

    # The "PostDeleteView" will handle the following route: localhost:8000/post/6/delete/
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # The about view will handle this path.
    path('about/', views.About, name='blog-about'),

    # The name of the template file for the following URL pattern would be "user_posts.html".
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),

    path('view-menu/', ViewMenu, name='view-menu'),

    # After creating a view, add a URL pattern, then create a template inside
    # the "app_name -> templates -> app_name_within_template_directory" directory.
]

# 33
