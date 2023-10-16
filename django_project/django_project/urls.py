from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
# Directly use the view from the "users" app by importing it.
from users import views as user_views

# The URL routes in this file support many of the navigations in the subapps of
# the entire web application.
urlpatterns = [
    path('admin/', admin.site.urls, name='admin:index'),

    # If the blog home page were to be made the home page for the entire website,
    # I would have to include the following code:
    # path("", include('blog.urls'))

    # If someone enters in 'http://localhost:8000/register/' as a url, then they will be sent
    # to the register view. Furthermore, each URL pattern can be assigned a name.
    path('register/', user_views.Register, name='register'),
    # Navigating to 'profile/', is handled by the user_views.profile view.
    path('profile/', user_views.Profile, name='profile'),

    # Django will look for the login template in the following directory: 'users/login.html'
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('facial-login/', user_views.FacialLogin, name='facial-login'),
    path('facial-login-result/', user_views.FacialLoginResult,
         name='facial-login-result'),
    path('capture-facial-image/', user_views.CaptureFacialImage,
         name='capture-facial-image'),

    # http://localhost:8000/blog/ will first reference the 'blog/' path in the
    # django_project.urls file.
    # Then the 'blog/' path in django_project.urls will map to the 'blog.urls' module.
    # In blog.urls there is a route for the home page handled by the "Home" function in
    # "blog.views". "include" will analyse anything after "blog" because of the first
    # argument for the "path" function. In this case, an empty string would be sent to
    # blog.urls.
    path('', include('blog.urls')),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'),
         name='password_reset'),

    # The third argument in path() is the url name that the login HTML template
    # will use in the case of someone forgetting their password. The login template
    # will use 'password-reset' to display the "password_reset.html" template.

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    # When "<>" is included in the first argument of the path() function,
    # it means that the url is accepting two url parameters.
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    # The last argument in the path() function is the name of the route.
    # Every template referenced in the second argument of the path() function
    # must have "View" at the end.

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    # With each of the following paths, the specific subapplications
    # handle the URL routings.
    path('', include('weather.urls')),
    path('', include('map_app.urls')),
    path('', include('Exams.urls', namespace='Exams')),
    path('', include('base.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'users.views.Error404View'

# This URLs module is in the main project directory. A particular pattern will
# tell the website which URLs should direct a user to the "blog" application.

# If in DEBUG mode, add the following two specific url patterns.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

# 56
