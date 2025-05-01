from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# In order to have a form create a new
# user, the "UserCreationForm" which
# Django provides, is taken advantage of.
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
import cv2
import os
import face_recognition
from pathlib import Path

'''
This file holds the view function that are
responsible for handling the GET and POST
requests for the "users" application.

A view which will handle the logic for the
"users.apps.UserConfig" route in the
"users/settings.py" file, must be created.'''


"""
Register()

NAME

	Register - handles an HttpRequest to the
	'register/' address.

SYNOPSIS

  def Register(request):
		request        --> the HttpRequest object
		which Django uses to pass
		state through the system.

DESCRIPTION

	Register() is the view for registering an account.

	This function accepts a web request. If it accepts
  a POST request, that indicates that data was sent
  after the user clicked the "Sign Up" button.
	In this case, the function will grab the
  "UserRegisterForm()" with the data in the POST
	request (request.POST) being passed as an argument
	to the form.

	If the form data is valid, it will be saved which
  means that a new profile has been created.

	The validated form data will be in the
  "form.cleaned_data" dictionary. .get('username')
	will return the value of the "username" input
	field which is determined based on user input.

	Then the user is redirected to the 'login' page.

	In the instance of this view accepting a GET request,
  it means that the user has chosen to register a new
  account with the web application. The user will be
  prompted to enter in a username, email, password,
	and then re-enter their password.

RETURNS

	Returns an HttpResponse object while rendering the
  'register.html' template located inside the "users"
  application. The "UserRegisterForm()" is rendered
	out with the "register.html" template.

"""


def Register(request):
	'''
	Having a nested if statement is necessary here
	because an object of the "UserRegisterForm" class
	must be verified as valid before being saved, and
	saving a "UserRegisterForm" object is only applicable
	if this view function has received a POST request.

	If a "POST" request is received, validate the form
	data which can be done with a conditional.'''
	if request.method == 'POST':
		# Create a new form that has the data
		# that was within "request.POST".

		# The data in this case is
		# the username and password.
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			# This line creates a new user
			# if the form is valid.
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(
				request,
				f'Your account has been created! You are now able to log in.'
			)
			# Users will be redirected to the 'login'
			# page after creating an account.
			return redirect('login')
	else:
		'''
		If a "GET" request is received, then create an
		instance of the form which will be passed to the
		template that was created for this view.

		Create a blank form for anything that is not a
		POST request.'''
		form = UserRegisterForm()
			
	'''
	Render this by passing the template as the second
	argument for the render() function.

	Pass the form as the third argument, so that the
	form can be accessed from within the "register.html"
	template. "form" is the instance of the
	UserCreationForm() that was created above.'''
	return render(request, 'users/register.html', {'form': form})

	# Have a blank form prepared for any requests that
	# come into the route of 'users/register.html'.
# def Register(request):


"""
Profile()

NAME

  Profile - handles an HttpRequest to the 'profile/'
	address.

SYNOPSIS

  def Profile(request):
    request        --> the HttpRequest object which
		Django uses to pass state through the system.

DESCRIPTION

  Profile() is the view for accessing an account's
	profile page or updating an account's profile
	details.

  "@login_required" ensures that the user must be
	logged-in to access the 'profile' page.

	This function accepts a web request. If it
	accepts a POST request, it means that the user
	has clicked the "Update" button on the 'profile'
	page. This will trigger a POST request whether
	the user has actually updated any of their profile
	details or not.

	If the form data for the UserUpdateForm() and
  ProfileUpdateForm() forms is valid, the data will
	be saved which means that the profile has been
	updated. Proceeding this, the user will be
	redirected back to the 'profile' page.

	In the instance of this view accepting a GET
	request, it means that the user has requested
	to view the 'profile' page where they will see
	their username, email, profile image, and facial
	image. They will still be able to update any of
	these attributes in this instance.

	This function will handle a GET request by passing
	the instance of the current logged-in user or
  "instance=request.user" to the UserUpdateForm() and
  ProfileUpdateForm() forms.

RETURNS

  Returns an HttpResponse object while rendering the
  'profile.html' template located inside the "users"
  application. The UserUpdateForm() and
	ProfileUpdateForm() forms are both rendered out
	with the "profile.html" template.

"""


@login_required
def Profile(request):
	if request.method == 'POST':
		'''
		"instance=request.user" is an instance of a user.
		An instance of a user must be passed to the form,
		so that the form can be populated with the
		information of the logged in user. The
		"UserUpdateForm" will have the email and username
		filled in. "request.POST" is the post data being
		sent to the form.'''
		u_form = UserUpdateForm(request.POST, instance=request.user)

		'''
		"instance=request.user.profile" is an instance of
		a profile. The "ProfileUpdateForm" will have the
		current image filled in. "request.FILES" will store
		the image that the user tries to upload for their
		profile picture.'''
		p_form = ProfileUpdateForm(
			request.POST, request.FILES, instance=request.user.profile
    )

		'''
		A nested if statement is necessary here because
		objects of the "UserRegisterForm" and
		"ProfileUpdateForm" classes must be verified as
		valid before being saved. Saving "UserRegisterForm"
		and "ProfileUpdateForm" objects is only applicable
		if this view function has received a POST request.

		If the data is valid for the "UserUpdateForm" and
		the "ProfileUpdateForm" the data will be saved.'''
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')

			return redirect('profile')
			'''
			Redirect the form back to the profile page
			because the form must not execute the "return render()"
			function call below because currently it is in a
			POST request and shouldn't run another POST request.
			"return redirect()" will run a GET request instead.'''
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form
	}
	# Pass "context" into the render() function, so
	# that it is accessible in the HTML template.
	return render(request, 'users/profile.html', context)
# def Profile(request):


"""
FacialLogin()

NAME

  FacialLogin - handles an HttpRequest to the
  'facial-login/' address.

SYNOPSIS

	def FacialLogin(request):
		request        --> the HttpRequest object which
		Django uses to pass state through the system.

DESCRIPTION

  This function will accept a web request, and will
  then return a web response. It takes an HttpRequest
  object which is its parameter, and returns it while
  rendering the HTML template titled 'facial_login.html'.

RETURNS

  Returns an HttpResponse object while rendering the
  'facial_login.html' template located inside the
  "users" application.

"""


def FacialLogin(request):
  return render(request, 'users/facial_login.html')
# def FacialLogin(request):


"""
FacialLoginResult()

NAME

  FacialLoginResult - handles an HttpRequest to the
  'facial-login-result/' address.

SYNOPSIS

	def FacialLoginResult(request):
		request        --> the HttpRequest object which
    Django uses to pass state through the system.

DESCRIPTION

	This function acquires the facial image submitted
  by a user which is supposed to be detected in the
  "submitted_facial_image.jpg" file.

	If the "submitted_facial_image.jpg" does not contain
  a face, the user will be informed of this with a web
  page stating so.

	It also obtains all of the facial images set by
  administrators which are stored inside the
  "facial_images" directory.

	While looping through the images inside the
  "facial_images" directory, the "face_recognition"
  tool in Python is used to check if the face in each
  image matches the face in the "submitted_facial_image.jpg"
  file which is converted and resized to be assigned
	to the "downloadedImg" variable. Each image in the
	"facial_images" directory undergoes the same process.

	If there is at least one match, the loop will be
	exited and "True" will be assigned to the
  "facialImageMatchedAtleastOnce" boolean variable.
  Otherwise, this variable will maintain the value of
	"False".

  This variable is sent to the "facial_login_result.html"
  template, so that it can output appropriate feedback.

	If an image in the "facial_images" directory does not
  contain a face, the for loop will skip it.

RETURNS

  Returns an HttpResponse object containing a Python
  dictionary that holds a boolean variable which is
  assigned a value based on whether the facial image
  submitted by the user, "downloadedImg", matches one
  of the facial images set by an administrator.

  The boolean variable will be accessible inside the
  'facial_login_result.html' template which is rendered
  and located inside the "users" application.

"""
# The following function is less than 100 lines.


def FacialLoginResult(request):
	# Load the images and convert them to RGB.
	# Images are retrieved as PGR, but the
	# library understands them as RGB.

	width = 300
	height = 300
	newDimensions = (width, height)

	# Get the path for the "Downloads" folder
	# on the user's local file system.
	downloadsFolderPath = str(Path.home() / "Downloads")

	try:
		downloadedImg = face_recognition.load_image_file(
			f'{downloadsFolderPath}/submitted_facial_image.jpg')
	except:
		return render(
			request, 'users/no_downloaded_image_error.html')

	downloadedImg = cv2.cvtColor(
		downloadedImg, cv2.COLOR_BGR2RGB)

	downloadedImg = cv2.resize(
		downloadedImg, newDimensions,
		interpolation=cv2.INTER_AREA)

	"""
	First check if the 'dlib' face detector was able
	to find a face in the image.

	If the image contains a face that is turned too
	sideways rather than looking straight into the
	camera, then the 'dlib' face detector might not
	detect the face."""
	if len(face_recognition.face_encodings(downloadedImg)) > 0:
		print("Success! A face was detected in the image "
					"that was downloaded.")
	else:
		print("Error! A face was not detected in the image "
					"that was downloaded.")

		'''
		A nested if statement is needed here because if a
		face was not detected in the image file downloaded
		by the user, that image file which is titled
		"submitted_facial_image.jpg", should be deleted.

		The reason why the image file is being deleted here
		is because if there is no face in the image, the
		"facial_login_result.html" template is rendered
		immediately afterwards.'''
		if os.path.exists(
			f'{downloadsFolderPath}/submitted_facial_image.jpg'
		):
			os.remove(
				f'{downloadsFolderPath}/submitted_facial_image.jpg')

			faceNotDetectedInDownloadedImage = True

			context = {
				'faceNotDetectedInDownloadedImage':
					faceNotDetectedInDownloadedImage
			}

			return render(
				request, "users/facial_login_result.html", context)
		
			'''
			Here it makes sense to terminate the program
			because if there was no face detected in the
			downloaded image, then it will not match any of
			the user images that are located inside the
			"django_project/media/facial_images" directory.'''

	# Load each image file into a numpy array,
	# which is a grid of non-negative values.
	# adminFacialImage = face_recognition.load_image_file(
	# 	f'{os.getcwd()}/media/facial_images/deniz.jpg')

	facialImagesFolderPath = f"{os.getcwd()}/media/facial_images"

	# Get all of the files inside the
	# 'facial_images' directory.
	facialImages = os.listdir(facialImagesFolderPath)

	print(f"facial_images: {facialImages}")

	facialImageMatchedAtleastOnce = False

	for facialImage in facialImages:
		adminFacialImage = face_recognition.load_image_file(
			f'{os.getcwd()}/media/facial_images/{facialImage}')

		adminFacialImage = cv2.cvtColor(
			adminFacialImage, cv2.COLOR_BGR2RGB)

		adminFacialImage = cv2.resize(
			adminFacialImage, newDimensions,
			interpolation=cv2.INTER_AREA)

		"""
		Find the faces in the images as well as their
		encodings.

		Because only a single image is being sent, only
		the first image of 'adminFacialImage' will be
		returned."""

		if len(face_recognition.face_encodings(adminFacialImage)) > 0:
			print("Success! A face was detected for this" \
						" particular admin image.")
		else:
			print("Error! A face was not detected in this" \
						" particular admin image.")
			# Skip to the next iteration.
			continue
			'''
			The program must not be terminated here because
			all of the other user images must still be checked
			to see if they not only contain a facial image, but
			that they also match the face in the downloaded image.'''

		# "faceLoc" will be returned an array that
		# contains the coordinates of each face.
		# Send in an image.
		faceLoc = face_recognition.face_locations(adminFacialImage)[0]

		# Encode the face that has been detected.
		encodeUser = face_recognition.face_encodings(adminFacialImage)[0]

		# See where the face has been detected.
		cv2.rectangle(adminFacialImage, (faceLoc[3], faceLoc[0]),
			(faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

		# Send in an image.
		faceLocTest = face_recognition.face_locations(downloadedImg)[0]

		# Encode the face that has been detected.
		encodeTest = face_recognition.face_encodings(downloadedImg)[0]

		# See where the face has been detected.
		cv2.rectangle(downloadedImg, (faceLocTest[3], faceLocTest[0]),
			(faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)

		# If the two facial images are to be displayed.
		# cv2.imshow("User Facial Image: ", adminFacialImage)
		# cv2.imshow("Downloaded Image: ", downloadedImg)

		result = face_recognition.compare_faces(
			[encodeUser], encodeTest)

		print("result: ", result)

		# If the face in the downloaded image matches
		# at least one of the faces in the "", the
		# loop will terminate.
		if result == [True]:
			facialImageMatchedAtleastOnce = True
			break

	context = {
		'facialImageMatchedAtleastOnce':
			facialImageMatchedAtleastOnce,
	}

	print('facialImageMatchedAtleastOnce: ',
		facialImageMatchedAtleastOnce)

	'''
	If the "submitted_facial_image.jpg" file has not
	been removed yet, it will be removed to avoid
	confusion with future images from the JavaScript
	canvas which will be saved inside the "Downloads"
	folder of the local file system.'''
	if os.path.exists(
		f'{downloadsFolderPath}/submitted_facial_image.jpg'):
		os.remove(
			f'{downloadsFolderPath}/submitted_facial_image.jpg')

	return render(
		request, 'users/facial_login_result.html', context)
# def FacialLoginResult(request):


"""
CaptureFacialImage()

NAME

  CaptureFacialImage - handles an HttpRequest to
	the 'set-facial-image/' address.

SYNOPSIS

	def CaptureFacialImage(request):
		request        --> the HttpRequest object which
		Django uses to pass state through the system.

DESCRIPTION

	This function will accept a web request, and will
	then return a web response. It takes an HttpRequest
	object which is its parameter, and returns it while
	rendering the HTML template titled 'set_facial_image.html'.

	"@login_required" simply ensures that the user is
	logged in before they access the 'set-facial-image'
	URL. If they are not logged in and they attempt to
	access this URL, they will be redirected to the login
	page.

RETURNS

  Returns an HttpResponse object while directing the
	user to the 'capture_facial_image.html' template
	located inside the "users" application.

"""


@login_required
def CaptureFacialImage(request):
  return render(request, 'users/capture_facial_image.html')
# def CaptureFacialImage(request):


"""
Error404View()

NAME

  Error404View - handles an HttpRequest to the an unknown
	address.

SYNOPSIS

  def Error404View(request, exception):
		request        --> the HttpRequest object which
		Django uses to pass state through the system.
		exception      --> the Http404 exception that is
		caught when a user attempts to request a URL that
		does not exist.

DESCRIPTION

	This function will accept a web request, and then will
	return a web response. It takes the HttpRequest object
	which is its parameter, and returns it while rendering
	the HTML template titled '404.html'.

RETURNS

	Returns an HttpResponse object while directing the user
	to the '404.html' template located inside the "users"
	application.

"""

def Error404View(request, exception):
  return render(request, '404.html')
# def Error404View(request, exception):

# 135