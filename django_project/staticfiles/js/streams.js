console.log('Stream.js connected');

/* This file is responsible for the back end
   operations of the "base" application which
   includes developing a working program where
   users can create a video meeting room, have
   other users join it, and communicate with
   other users via audio while having the
   computer's camera turned on for seeing the
   faces of other users.

   The client object will give functions for
   voice and video calls. 'codec' is the
   encoding method that the browser will use. */
const g_Client = AgoraRTC.createClient({ codec: "vp8", mode: "rtc" });

/* "g_APP_ID" is simply the app ID that was
   generated when I created a project for
   the chat room on Agora's website. */
const g_APP_ID = '16c106d4fb6b4161b6230b94fec2d5a4';

/* For the purpose of making a video call,
   Agora will provide the option to create
   a channel and a token to authenticate
   the channel.
  
   Get the channel name from the session. */
const g_CHANNEL = sessionStorage.getItem('room');

/* Retrieving "token" from sessionStorage is
   more efficient because if I was to hardcode
   the token from the Agora channel, I would
   need to update it every twenty-four hours. */
const g_TOKEN = sessionStorage.getItem('token');

let g_userID = sessionStorage.getItem('userID');

/* Permission for the browser to retrieve audio
   and video tracks will be stored in the
   "LocalTracks" array. The "RemoteUsers" array
   will store the same for remote users. */
let LocalTracks = [];
let RemoteUsers = {};

/*
JoinAndDisplayLocalStream = async () =>

NAME

  JoinAndDisplayLocalStream - stores the local
  audio and video tracks as well as the tracks
  for remote users who join a meeting room.

SYNOPSIS

  let JoinAndDisplayLocalStream = async () =>
    This function does not have any parameters.

DESCRIPTION

  This function takes the "APP_ID", "CHANNEL",
  and "TOKEN" to join a  specific channel with
  the "client" object.

  A user's audio and video tracks are retrieved,
  and stored inside the "LocalTracks" array.

  For the purpose of being able to identify
  which video player is associated with each
  user, the "g_userID" is included in the id
  property of the each video player element.
  
  The video player element which is named "player",
  is appended to the Document Object Model by
  being added to the beginning of the
  "video-streams" wrapper.

  The play() method is then called by the video
  track "LocalTracks[1]" to begin the playback.

  The tracks are then published, so that other
  users inside a channel have access to the
  user's audio and video tracks.

RETURNS

  While nothing is returned, this function
  appends a video player element to a stream,
  plays user's video track, and finally
  publishes a user's audio and video tracks
  to the specific channel they are joining.

*/
let JoinAndDisplayLocalStream = async () => {
  /* Assign the channel name to
     the 'room-name' element. */
  document.getElementById('room-name').innerText = g_CHANNEL;

  /* During the time that the publish(LocalTracks[0],
     LocalTracks[1]) method is called, event listeners
     will have the users in the stream listen to the
     event, and call the 'user-published()' method.

     Whenever the publish(LocalTracks[0], LocalTracks[1])
     method is called, the HandleUserJoined() method
     will have access to the audio and video tracks
     of a certain user. This works by using that
     information to create a video player and display
     it in a web browser.
    
     The following line acts as an event listener for
     the publish(LocalTracks[0], LocalTracks[1]) method.
     
     HandleUserJoined() will handle the event. */
  g_Client.on('user-published', HandleUserJoined);

  /* The 'user-left' method is when a
     user leaves the chat stream. */
  g_Client.on('user-left', HandleUserLeft);

  /* There is a try-catch block here because if
     there is no chat session, the user will be
     redirected back to the home page. */
  try {
    /* Here the g_Client.join() method is being
       called because I must access the client
       object which was declared above as 'g_Client'.

       The purpose of this is to join a channel with
       the necessary credentials.

       In the join() method below, the 'g_APP_ID',
       'g_CHANNEL', and 'g_TOKEN' are joining a
       channel. */
    g_userID = await g_Client.join(g_APP_ID, g_CHANNEL, g_TOKEN, g_userID);
  } catch (a_error) {
    console.error(a_error);

    // The subsequent line will send the
    // user back to the home page.
    // window.open('/', '_self')
  }

  /* Set 'LocalTracks' to the audio and video
     tracks of a user.

     LocalTracks[0] will hold the audio track.
     LocalTracks[1] will hold the video track. */
  LocalTracks = await AgoraRTC.createMicrophoneAndCameraTracks();

  /* Get a member from the return value
     in the CreateMember() function. */
  let member = await CreateMember();

  /* Create a video player anytime a user joins
     a meeting.
     
     ${g_userID} must be factored in when creating
     a video play because it must be known which
     video player is associated with each user.

     Each user's ID will be unique since their
     'g_userID' is used to generate their ID. */
  let player = `
    <div class="video-container" id="user-container-${g_userID}">
      <div class="username-wrapper">
        <span class="user-name">${member.name}</span>
      </div>

      <div class="room-name-wrapper">
        <span class="room-name">Room Name: ${g_CHANNEL}</span>
      </div>

      <div class="video-player" id="user-${g_userID}"></div>
    </div>`

  /* Append the video player to the DOM (Document
     Object Model) called 'video-streams'. Putting
     'beforeend' in the first argument will make
     sure that the video player gets added to the
     beginning of the Java wrapper. */
  document.getElementById('video-streams').insertAdjacentHTML('beforeend', player);
  LocalTracks[1].play(`user-${g_userID}`);

  /* Publish the audio and video tracks of
     the user to a particular channel. */
  await g_Client.publish([LocalTracks[0], LocalTracks[1]]);
}
/*let JoinAndDisplayLocalStream = async () => */

/*
HandleUserJoined = async () =>

NAME

  HandleUserJoined - creates a video player for
  a user if the user does not already have one.

SYNOPSIS

  let HandleUserJoined = async (a_user, a_mediaType) =>
    a_user             --> the user object
    representing the user who joins a stream.
    a_mediaType        --> the type of media
    (either "video" or "audio").

DESCRIPTION

  This function first adds the user object "a_user"
  to the dictionary container called "RemoteUsers".

  The local "client" object will be subscribed
  to the user joining the stream.

  If "mediaType" is equal to 'video', the user's
  video is used to generate a video player, and
  display it in the Document Object Model only if
  the video player for that specific user doesn't
  already exist.

  In this context, it is not a local track being
  retrieved and played, but a user's tracks.

  If the "mediaType" is an audio track, the audio
  is played as well.

RETURNS

  While nothing is returned, this function
  appends a video player element to a stream,
  plays user's video track, and finally
  publishes a user's audio and video tracks
  to the specific channel they are joining.

*/
let HandleUserJoined = async (a_user, a_mediaType) => {
  /* "user.uid" is the key and
     "user" is the value. */
  RemoteUsers[a_user.uid] = a_user;

  /* The local client object is
     subscribing to the user. */
  await g_Client.subscribe(a_user, a_mediaType);

  /* If the second parameter of this function is
     a media of type "video", it is essential to
     remove a user's video player if it still exists
     in a DOM from a previous session. The reason
     why this must be done inside a nested if
     statement, is because other actions must also
     occur after it has been verified that the media
     type is "video". */
  if (a_mediaType === 'video') {
    let player = document.getElementById(`user-container-${a_user.uid}`);

    /* This conditional statement is used to
       ensure that there isn't a video player
       already in the DOM (Document Object Model).
       
       If there is an old video player already,
       it will be removed. */
    if (player != null)
      player.remove();

    let member = await GetMember(a_user);

    // Here the video source is being
    // appended to the DOM.
    player = `
      <div class="video-container" id="user-container-${a_user.uid}">
        <div class="video-player" id="user-${a_user.uid}"></div>
          <div class="username-wrapper">
            <span class="user-name">${member.name}</span>
          </div>

          <div class="room-name-wrapper">
            <span class="room-name">Room Name: ${g_CHANNEL}</span>
          </div>
      </div>`

    document.getElementById('video-streams').
      insertAdjacentHTML('beforeend', player);

    /* The play() method will create a video tag as
       an HTML element, and will play the video
       inside of that video tag. For this reason,
       the "g_userID" of each user must be unique.
       
       The play() method will be passed the ID of each
       user because the user ID is inside the document
       object model. */
    a_user.videoTrack.play(`user-${a_user.uid}`);
  }

  if (a_mediaType === 'audio')
    a_user.audioTrack.play();
}
/*let HandleUserJoined = async (a_user, a_mediaType) => */

/*
HandleUserLeft = async () =>

NAME

  HandleUserLeft - takes the necessary actions
  when a user leaves a stream.

SYNOPSIS

  let HandleUserLeft = async (a_user) =>
    a_user        --> the user object representing
    the user who joins a stream.

DESCRIPTION

  This function will remove a user from the
  "RemoteUsers" dictionary container by using
  its key.

  The user object's audio and video tracks
  will be stopped, and they will be removed
  from the Document Object Model.

RETURNS

  This function does not return anything, but
  instead plays an important role in handling
  a user object leaving a meeting room by
  removing them from the dictionary container
  where they are inserted when a user joins a
  channel.

*/
let HandleUserLeft = async (a_user) => {
  /* Remove each user from the "RemoteUsers"
     dictionary by their unique key. */
  delete RemoteUsers[a_user.uid];

  /* Remove the user from the Document
     Object Model by their unique key. */
  document.getElementById(`user-container-${a_user.uid}`).remove();
}
/*let HandleUserLeft = async (a_user) => */

/*
LeaveAndRemoveLocalStream = async () =>

NAME

  LeaveAndRemoveLocalStream - manages a
  user's audio and video tracks when they
  leave a stream.

SYNOPSIS

  let LeaveAndRemoveLocalStream = async () =>
    This function does not accept any parameters.

DESCRIPTION

  This function is responsible for looping
  through all of the audio and video tracks,
  closing them, and then unsubscribing from
  the channel channel stream that was initially
  joined.

  The stop() method stops a tracks. To launch
  the track again, it must be opened up again.
  Before opening up the track again, it must be
  closed which is why the close() method is
  called afterwards.

RETURNS

  This function does not return anything, but
  instead has the "client" object leave a
  channel, and directs a user back to the
  'lobby' page of the "base" application.

*/
let LeaveAndRemoveLocalStream = async () => {
  for (let track = 0; LocalTracks.length > track; track++) {
    LocalTracks[track].stop();
    LocalTracks[track].close();
  }

  /* Leave the channel stream. */
  await g_Client.leave();

  /* Deletes a "RoomMember" object if the user has
     left the meeting room or closed their window. */
  DeleteMember();

  /* The following path has a "/" before "lobby"
     because I wanted to put the 'lobby' address
     in the URL address bar without having "room/"
     stay in the URL address bar before it. */
  window.location.href = "/lobby";
}
/*let LeaveAndRemoveLocalStream = async () => */

/*
ToggleCamera = async () =>
 
NAME
 
  ToggleCamera - makes the camera button
  function properly, so that a user can
  turn their camera on and off during while
  they are in a meeting room.
 
SYNOPSIS
 
  let ToggleCamera = async (a_event) =>
    a_event        --> the event which in this
    case is the camera button clicked by the user.
 
DESCRIPTION
 
  This function first checks if the local
  video track is muted.

  If "LocalTracks[1].muted" is true, it
  means that the user's camera is off.

  If the user's camera is off, this function
  will turn it on, and set the camera button's
  colour to white ('#fff').

  If the user's camera is currently on, it will
  be turned off, and the camera button's colour
  will be set to red. This makes sense because
  the button that triggers this function is
  responsible for turning a user's camera on
  and off.

RETURNS
 
  Nothing needs to be returned by this function
  as its responsibility is to change the status
  of a user's video background as well as the
  colour of their camera button when it is clicked.
 
*/
let ToggleCamera = async (a_event) => {
  console.log('ToggleCamera() Function Triggered');

  /* Check if the video track is muted. */
  if (LocalTracks[1].muted) {
    /* setMuted(false) will turn the camera on. */
    await LocalTracks[1].setMuted(false);

    /* "a_event" represents the event. Here the
       background is being set to the colour
       white upon the start of the event. */
    a_event.target.style.backgroundColor = '#fff';
  } else {
    /* If the camera is on, it will be turned
       off by setting 'setMuted' to true. */
    await LocalTracks[1].setMuted(true);
    a_event.target.style.backgroundColor = 'rgb(255, 80, 80, 1)';
  }
}
/*let ToggleCamera = async (a_event) => */


/*
ToggleMic = async () =>
 
NAME
 
  ToggleMic - makes the microphone button
  function properly, so that a user can
  turn their audio on and off during while
  they are in a meeting room.
 
SYNOPSIS
 
  let ToggleMic = async (a_event) =>
    a_event        --> the event which in this
    case is the microphone button clicked by
    the user.
 
DESCRIPTION
 
  The function for ToggleMic() is almost
  identical to the function ToggleCamera().

  The only difference is the status of a
  user's audio track "LocalTracks[0]" is
  being changed whereas the ToggleCamera()
  function changes the status of a user's
  video track.

  This function first checks if the local
  audio track is muted.

  If "LocalTracks[0].muted" is true, it
  means that the user's audio is off.

  If the user's microphone is off, this
  function will turn it on, and set the
  microphone button's colour to white ('#fff').

  If the user's microphone is currently on,
  it will be turned off, and the microphone
  button's colour will be set to red. This
  makes sense because the button that
  triggers this function is responsible for
  turning a user's audio on and off.

RETURNS
 
  Nothing needs to be returned by this
  function as its responsibility is to
  change the status of a user's audio
  as well as the colour of their
  microphone button when it is clicked.
 
*/

let ToggleMic = async (a_event) => {
  console.log('ToggleMic() Function Triggered');

  if (LocalTracks[0].muted) {
    await LocalTracks[0].setMuted(false);
    a_event.target.style.backgroundColor = '#fff';
  } else {
    await LocalTracks[0].setMuted(true);
    a_event.target.style.backgroundColor = 'rgb(255, 80, 80, 1)';
  }
}
/*let ToggleMic = async (a_event) => */

/* Get the name of the user
   who joined the session. */
let g_NAME = sessionStorage.getItem('name');

/*
CreateMember = async () =>
 
NAME
 
  CreateMember - sends a request from the
  front end to the back end to create a
  "RoomMember" object.
 
SYNOPSIS
 
    let CreateMember = async () =>
        This function does not accept any parameters.
 
DESCRIPTION
 
  This function first makes a POST request
  using the fetch() function to the
  '/create_member/' address. The CreateMember()
  view function located in the "django_project/
  base/views.py" file is where the JSON data
  from the front end is coming from.

  The data being sent with the POST request is
  the name of the user, the meeting room name,
  and the user ID. This is possible because
  "g_NAME", "g_CHANNEL", and "g_userID" are all
  set in a session within this file.

  The response returned back is waited for.
  When the response is received, a "RoomMember"
  object is returned.

  The CreateMember() function must be asynchronous
  because a request is being sent from the front
  end and a user will be created.
 
RETURNS
 
  After this function creates a new "RoomMember"
  object in the database, it returns it.
 
*/

let CreateMember = async () => {

  /* A POST request is being sent here. */
  let response = await fetch('/create_member/', {
    method: 'POST',
    headers: {
      /* Specify that json data is being dealt with. */
      'Content-Type': 'application/json'
    },
    /* Append the data to the request body, but first
       convert the JavaScript object to a JSON string. */
    body: JSON.stringify({ 'name': g_NAME, 'roomName': g_CHANNEL, 'userID': g_userID })
  })

  /* Wait for the server to respond, and parse
     the body text as a JSON object. */
  let member = await response.json();

  return member
}
/*let CreateMember = async () => */

/*
GetMember = async () =>
 
NAME
 
  GetMember - sends a request from the front end
  to the back end for the sake of a obtaining a
  specified member.
 
SYNOPSIS
 
  let GetMember = async (a_user) =>
    a_user        --> a specific user which will
    aid this function in finding the appropriate
    "RoomMember" object.

DESCRIPTION
 
  This function will use the fetch() method
  to make a request to the '/get_member/
  ?userID=${a_user.uid}&roomName=${g_CHANNEL}'
  address.

  The data from the front end is coming from
  the GetMember() view function located in the
  "django_project/base/views.py" file.

  A member being found is based on the "a_user"
  parameter. The unique user ID "uid" is a member
  of the "a_user" object.

  Since a user will already be in the stream,
  the "g_CHANNEL" variable from the session
  can be utilised to find the correct name of
  the meeting room that the user has joined.

RETURNS
 
  The "RoomMember" object acquired
  by this function is returned.
 
*/
let GetMember = async (a_user) => {
  let response = await fetch(
    `/get_member/?userID=${a_user.uid}&roomName=${g_CHANNEL}`)

  let member = await response.json()

  return member
}
/*let GetMember = async (a_user) => */

/*
DeleteMember = async () =>
 
NAME
 
  DeleteMember - makes a POST request to delete
  a member whenever a user leaves a meeting room
  of closes their window.
 
SYNOPSIS
 
  let DeleteMember = async () =>
    This function does not accept any parameters.
 
DESCRIPTION
 
  This function will use the fetch() method to
  make a request to the '/delete_member/' address.

  The request in this case is a POST request
  where the name of a member, room name, and
  user ID are sent.

  Those three pieces of data are received by the
  DeleteMember() function defined in the
  "django_project/base/views.py" file.
  
  The DeleteMember() function will load the three
  data components mentioned above as JSON data,
  and will then use them to get a "RoomMember" object.

  Finally, the DeleteMember() function will delete
  the particular object it has obtained from the
  data sent from this function.

RETURNS
 
  Nothing is returned by this function as its
  sole task is to send the accurate data to
  the DeleteMember() function, and then wait
  for a response from the DeleteMember() function.
  By then, the specific "RoomMember" object
  will have been deleted.

*/
let DeleteMember = async () => {
  let response = await fetch('/delete_member/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(
      { 'name': g_NAME,
        'roomName': g_CHANNEL,
        'userID': g_userID })
  })

  let member = await response.json();
}
/*let DeleteMember = async () => */

window.addEventListener("beforeunload", DeleteMember);

/* This method will be called when
   a new user joins a channel. */
JoinAndDisplayLocalStream();

/* When the "leave-btn" element is clicked, the
   LeaveAndRemoveLocalStream() function will
   handle that event. The same logic applies to
   the "camera-btn" and "mic-btn" elements and
   their own event listeners. */
document.getElementById('leave-btn').addEventListener('click', LeaveAndRemoveLocalStream);
document.getElementById('camera-btn').addEventListener('click', ToggleCamera);
document.getElementById('mic-btn').addEventListener('click', ToggleMic);

/* 155 */