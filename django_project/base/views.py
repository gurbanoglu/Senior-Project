import random
from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
from .models import RoomMember
import time
import json
from django.views.decorators.csrf import csrf_exempt


# The views here will handle the GET and POST
# requests for the "base" application.

"""
GetToken()

NAME

    GetToken - generates the token necessary for client authentication.

    For each client to join a channel, they must be authenticated.

SYNOPSIS

    def GetToken(request):
        request        --> the HttpRequest object which Django uses to pass state
        through the system.

DESCRIPTION

    This function has access to the application ID and certificate which were
    created with my Agora project on the Agora website. The channel name is
    retrieved from the GET request.

    The user ID is assigned a random number between 1 & 230, and expires in 48
    hours. This means that a new room will need to be joined as the authentication
    token for each client will eventually expire.

    The token (RTC token) is generated with the assistance of the RtcTokenBuilder()
    function along with the "buildTokenWithUid" method.

RETURNS

    Returns a JsonResponse containing the authentication token as well as the user ID.

"""


def GetToken(request):
    appID = "16c106d4fb6b4161b6230b94fec2d5a4"
    appCertificate = "1fc278257c934afbabba3eb4c80af8c6"
    channelName = request.GET.get('channel')

    # The 'userID' will be a number between 1 and 230.
    userID = random.randint(1, 230)

    # The expiration time for the 'userID' is 3600 seconds * 48 (60 minutes * 48)
    # which equates to 48 hours.
    expirationTimeInSeconds = 3600 * 48

    # Here the current time stamp is being retrieved.
    currentTimeStamp = int(time.time())

    # Adding the expiration time to the current time stamp will equal
    # the correct time value that indicates when the 'userID' token is
    # supposed to expire.
    privilegeExpiredTimeStamp = currentTimeStamp + expirationTimeInSeconds

    # Assigning a value of one to 'role' marks this is as the host.
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appID, appCertificate, channelName,
                                              userID, role, privilegeExpiredTimeStamp)

    return JsonResponse({'token': token, 'userID': userID}, safe=False)
# def GetToken(request):


"""
Lobby()

NAME

    Lobby - handles an HttpRequest to the 'lobby/' address.

SYNOPSIS

    def Lobby(request):
        request        --> the HttpRequest object which Django uses to pass state
        through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'lobby.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 'lobby.html'
    template located inside the "base" application.

"""


def Lobby(request):
    return render(request, 'base/lobby.html')
# def Lobby(request):


"""
Room()

NAME

    Room - handles an HttpRequest to the 'room/' address.

SYNOPSIS

    def Room(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'room.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 'room.html'
    template located inside the "base" application.

"""


def Room(request):
    return render(request, 'base/room.html')
# def Room(request):


"""
CreateUser()

NAME

    CreateUser - receives JSON data needed to create a "RoomMember" object.

    If the "RoomMember" object already exists, a boolean variable will keep note 
    of this. In any case, the "RoomMember" object will be returned.

SYNOPSIS

    def CreateUser(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    The function will access data by parsing a JSON string and
    converting it into a Python dictionary which is what "data"
    is in this case.

    The keys in the Python dictionary will be used to assign the
    appropriate values to the following attributes:
    "m_name", "m_userID", "m_roomName"

RETURNS

    Returns a JsonResponse containing the name of the person joining
    the room as well as the "safe" parameter set to false which means
    that any object can be passed for serialisation.

"""


def CreateUser(request):
    # The data is being retrieved from the front-end and then either
    # a new room member will be created or if an existing room member
    # already has those same credentials, it means they already exist.
    data = json.loads(request.body)

    # If the object already exists, "created" will be false, otherwise,
    # "created" is true. Nevertheless, the "RoomMember" object is returned.
    member, created = RoomMember.objects.get_or_create(
        m_name=data['m_name'],
        m_userID=data['m_userID'],
        m_roomName=data['m_roomName']
    )

    return JsonResponse({'name': data['m_name']}, safe=False)
# def CreateUser(request):


"""
CreateMember()

NAME

    CreateMember - receives JSON data needed to create a "RoomMember"
    object.

    If the "RoomMember" object already exists, a boolean variable will keep note 
    of this. In any case, the "RoomMember" object will be returned.

    One notable difference between this view function and the one above it is
    that this function is exempt from the protection ensured by the CSRF middleware.

SYNOPSIS

    def CreateMember(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    The function will access data by parsing a JSON string and
    converting it into a Python dictionary which is what "data"
    is in this case.

    The keys in the Python dictionary will be used to assign the
    appropriate values to the following attributes:
    "m_name", "m_userID", "m_roomName"

    Including "@csrf_exempt" means that the view does
    not need a csrf token in order to receive data.

RETURNS

    Returns a JsonResponse containing the name of the person joining
    the room as well as the "safe" parameter set to false which means
    that any object can be passed for serialisation.

"""


@csrf_exempt
def CreateMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        m_name=data['name'],
        m_userID=data['userID'],
        m_roomName=data['roomName']
    )

    return JsonResponse({'name': data['name']}, safe=False)
# def CreateMember(request):


"""
GetMember()

NAME

    GetMember - grabs two different pieces of data assigned
    to two different parameters entered in a URL.

    The names of the parameters in the URL are the following:
    "userID", "roomName"

SYNOPSIS

    def GetMember(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    The function grabs the two parameters in the URL called "userID"
    and "roomName" and will assign their values to the attributes
    "m_userID" and "m_roomName" which make up the "RoomMember" model.

    The name of the user who joins the meeting room is declared as
    "m_name". "m_name" is the member of the object "member" since it
    is an instance of the "RoomMember" class.

    The name of the user established when retrieving a "RoomMember"
    object is then assignment to the variable "m_name".

RETURNS

    Returns a JsonResponse containing the name of the member who joined
    the room as well as the "safe" parameter set to false which means
    that any object can be passed for serialisation.

"""


def GetMember(request):
    userID = request.GET.get('userID')
    roomName = request.GET.get('roomName')

    member = RoomMember.objects.get(
        m_userID=userID,
        m_roomName=roomName,
    )
    m_name = member.m_name

    return JsonResponse({'name': member.m_name}, safe=False)
# def GetMember(request):


"""
DeleteMember()

NAME

    DeleteMember - receives JSON data needed to retrieve a
    particular "RoomMember" object.

    After providing the needed attributes to form a "RoomMember" object,
    the specific member is deleted.

SYNOPSIS

    def DeleteMember(request):
        request        --> the HttpRequest object which Django uses to
        pass state through the system.

DESCRIPTION

    The function will access data by parsing a JSON string and
    converting it into a Python dictionary which is what "data"
    is in this case.

    The keys in the Python dictionary are the following:
    "name", "userID", "roomName"

    The keys in the Python dictionary will be used to assign the
    appropriate values to the following attributes:
    "m_name", "m_userID", "m_roomName"

    An instance of the "RoomMember" class is being sought out in
    this case, so that it can be deleted.

    Including "@csrf_exempt", means that the view does
    not need a csrf token in order to receive data.

RETURNS

    Returns a JsonResponse containing text stating "Member Deleted"
    to notify the user that the member has been deleted, as well as
    the "safe" parameter set to false which means that any object
    can be passed for serialisation.

"""


@csrf_exempt
def DeleteMember(request):
    data = json.loads(request.body)

    member = RoomMember.objects.get(
        m_name=data['name'],
        m_userID=data['userID'],
        m_roomName=data['roomName']
    )
    member.delete()

    return JsonResponse('Member Deleted', safe=False)
# def DeleteMember(request):

# 64
