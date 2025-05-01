from django.shortcuts import render, get_object_or_404

'''
LoginRequiredMixin requires that a user be
logged in, in order to make a new post. If
a user is logged out and attempts to go to
"localhost:8000/post/new" they will be
redirected to the login page.'''

# UserPassesTestMixin is a class which allows us
# to restrict the permission of updating a post
# only to the author of the post.
from django.contrib.auth.mixins import (
  LoginRequiredMixin, UserPassesTestMixin
)

# Import the "User" model.
from django.contrib.auth.models import User

# The views handling the HTTP requests inside
# the "blog" app are defined here.

# Import specific views so that specific
# class-based views can be created.
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)

# The "." in front of models means the
# 'models' file in the current directory.
# Import the "Post" class.
from .models import Post

"""
Home()

NAME

	Home - handles the HttpRequest to the '/'
  address which is the homepage of the Django
  web application.

SYNOPSIS

	def Home(request):
		request        --> the HttpRequest object
    which Django uses to pass state through the
  	system.

DESCRIPTION

	The function will retrieve all of the objects
  of the "Post" class defined in "django_project/
  blog/models.py", and will store	them in a Python
  dictionary called "context". They key inside the
	dictionary is called "posts".

	The dictionary is then passed to the HTML template
  titled "home.html" where it is accessed to retrieve
  all of the posts published by users, so that they
  can be displayed on the website's home page.

	The final result is the homepage of the application
  being displayed.

RETURNS

	Returns an HttpResponse object while directing
	the user to the 'home.html' template located
	inside the "blog" application.

"""


def Home(request):
	context = {
		# Query all of the posts from the database.
		'posts': Post.objects.all()
	}

	'''
	The "posts" variable which is a list of dictionaries,
	is going to be accessible inside the home.html
	template because "context" was passed as a third
	argument inside the render function below.

	Here a render template is being returned instead
  of an HTTP response. However, in this case, the
  render function is still returning an HTTP response.

	"home.html" is the template that is being rendered
  for the home view.
  
  render(request, template_name)
	blog/template_name.html
  '''
	return render(request, 'blog/home.html', context)
# def Home(request):

# The class-based views will be looking for
# a template with the the following naming
# convention:
# <app>/<model>_<view_type>.html


# "PostListView" is the class-based view that was
# created to display the homepage of the website.
class PostListView(ListView):
	# Below I am telling the list view which model to
	# query, so that I can create the list. In this
	# case, the model to be queried is all of the posts.
	model = Post

	# <application>/<model>_<view_type>.html
	template_name = 'blog/home.html'

	# Tells the class-based view that I want the
	# variable to be called "posts" rather than
	# "object list" by default.
	context_object_name = 'posts'

	# Add an "ordering" attribute to order
	# the posts from newest to oldest.
	ordering = ['-m_datePosted']

	# To order the posts from oldest to newest:
	# ordering = ['m_datePosted']

	# Limit the number of posts displayed on
	# each page to 6:
	paginate_by = 6


class UserPostListView(ListView):
	# Create a filter that will only get posts
	# that were written from a specific user.
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'

	# Since I am overriding the query that the
	# "UserPostListView" will be making, I added
	# "order_by('-m_datePosted')" directly to the query.

	paginate_by = 6

	def get_queryset(self):
		'''
		Get an object from the "User" model.
		The user that needs to be retrieved is a user with
		the username that is equal to the username entered
		in the URL. If the user exists, I will capture them
		in the "user" variable. Otherwise, a 404 error is
		returned.

		This will limit posts being displayed on the page
		to the specific user who has their username as the
		parameter in the url.'''
		user = get_object_or_404(
			User, username=self.kwargs.get('username'))

		return Post.objects.filter(m_author=user).order_by('-m_datePosted')


class PostDetailView(DetailView):
  model = Post


# The "PostCreateView" will be a view with a form where a new post is created.
class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['m_title', 'm_content']

	def form_valid(self, form):
		# Before the form is submitted, take the instance and
		# set the author equal to the current logged in user.
		form.instance.m_author = self.request.user

		# Run the form_valid() method to validate the form.
		return super().form_valid(form)


# The "PostUpdateView" will be a view with
# a form where a new post is updated.
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['m_title', 'm_content']

	def form_valid(self, form):
		# Before the form is submitted, take the instance and
		# set the author equal to the current logged in user.
		form.instance.m_author = self.request.user

		# Run the form_valid() method to validate the form.
		return super().form_valid(form)

	def test_func(self):
		# Get the current post that is being updated.
		post = self.get_object()

		# "self.request.user" is the current logged in user.
		# Check if the current logged in user is equal to
		# the author of the post that is being updated.
		if self.request.user == post.m_author:
			return True

		# If the current logged in user is not equal to the
		# author of the post being updated then return false.
		return False


class PostDeleteView(
  LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post

	# Redirect to the homepage after deleting a post.
	success_url = '/'

	# Ensure that the user deleting the
	# post is the author of the post.
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.m_author:
			return True
		return False


"""
About()

NAME

	About - handles the HttpRequest to the '/'
	address which is the home page of the Django
	web application.

SYNOPSIS

	def About(request):
		request        --> the HttpRequest object
		which Django uses to pass state through the
		system.

DESCRIPTION

	The function will retrieve all of the objects of
	the "Post" class defined in "django_project/blog/models.py",
	and will store them in a Python dictionary called "context".

	The dictionary is then passed to the HTML template
	titled "home.html" where it is accessed to retrieve
	all of the posts published by users, so that they
	can be displayed on the website's home page.

RETURNS

	Returns an HttpResponse object while directing the
	user to the 'home.html' template located inside the
	"blog" application.

"""


def About(request):
	# Render the about.html template.
	# For this template, I gave it a title.
	return render(
		request, 'blog/about.html', {'title': 'About'})
# def About(request):


"""
ViewMenu()

NAME

  ViewMenu - handles the HttpRequest to the 'view-menu/' address.

SYNOPSIS

	def ViewMenu(request):
		request        --> the HttpRequest object
		which Django uses to pass	state through the
		system.

DESCRIPTION

	This function will accept a web request, and
	will then return a web response. It takes the
	HttpRequest object which is its parameter, and
	returns it while rendering the HTML template
	titled 'view_menu.html'.

RETURNS

	Returns an HttpResponse object while directing
	the user to the 'view_menu.html' template located
	inside the "map_app" application.

"""


def ViewMenu(request):
  return render(request, 'blog/view_menu.html')
# def ViewMenu(request):

# 89
