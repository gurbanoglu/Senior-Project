/*This JavaScript file is responsible for back end operations that
  permit the exam timer to function.

  The JavaScript in this file also accurately marks a user's exam answers
  as "Correct", "Incorrect", or "Not Answered".*/

const g_TimerBox = document.getElementById('timer-box');
const g_ZeroTimerBox = document.getElementById("zero-timer-box");

/*
ActivateTimer = () =>

NAME

    ActivateTimer - processes the limited time duration for each exam.

SYNOPSIS

    ActivateTimer = (a_time) =>
        a_time        --> the time limit for a specific exam which this
        function will count down from.

DESCRIPTION

    This function first establishes how long the time limit is for an exam
    in order to display proper time format.

    It then uses a built-in Javascript method called setInterval() to decrement
    the value of "seconds" every one-thousand milliseconds (one second).

    In the case of time running out, the timer box will be reset to zero zero,
    and the test taker will be notified.

RETURNS

    Despite this function not returning anything, the text that appears in
    the "g_TimerBox" will be updated every second after the exam has begun.

*/
const ActivateTimer = (a_time) => {
    g_ZeroTimerBox.style.display = "none";

    /*If the time limit is ten minutes, then the
      following condition will not be met.*/
    if (a_time.toString().length < 2)
        g_TimerBox.innerHTML = `<b>0${a_time}:00</b>`;
    else
        /*If the time limit is ten minutes or higher.*/
        g_TimerBox.innerHTML = `<b>${a_time}:00</b>`;

    let minutes = a_time - 1;
    let seconds = 60;
    let displaySeconds = 0;
    let displayMinutes = 0;

    const Timer = setInterval(() => {
        /*The "seconds" variable will decrement every second.*/
        seconds--;

        if (seconds < 0) {
            seconds = 59;
            minutes--;
        }

        if (minutes.toString().length < 2)
            displayMinutes = '0' + minutes;
        else
            displayMinutes = minutes;

        if (seconds.toString().length < 2)
            displaySeconds = '0' + seconds;
        else
            displaySeconds = seconds;

        /*In JavaScript, three equal signs means "equality without coercion"
          or strict equality. This will return true if only both the types and
          values are the same. In JavaScript, three equal signs is faster than
          two because with three equal signs, type conversions do not occur.*/
        if (minutes === 0 && seconds === 0) {
            /*Reset the timer box to zero zero after time has run out.*/
            g_TimerBox.innerHTML = "<b>00:00</b>";

            /*The following code will execute after 500 milliseconds
              or half a second.*/
            setTimeout(() => {
                /*clearInterval() is needed here to force the setInterval() 
                  to stop running.*/
                clearInterval(Timer);
                alert('Time has expired.');
                SendData();
            }, 500)
        }
        g_TimerBox.innerHTML = `<b>${displayMinutes}: ${displaySeconds}</b>`;
    }, 1000)
}
/*ActivateTimer = (a_time) => */

const g_URL = window.location.href;

/*Wrap 'exam-box' which was defined inside exam.html as an id,
   and assign the 'g_ExamBox' element to it which is declared here.*/
const g_ExamBox = document.getElementById('exam-box');

/*
$.ajax()

NAME

    $.ajax - formats the exam interface and calls a function to begin the timer
    count down of an exam.

SYNOPSIS

    $.ajax({ type: 'GET', url: `${g_URL}data`, success: function (response){}, 
             error: function(a_error){} })
        type        --> the type of the HTTP method.
        url         --> the string containing the URL to which the request is sent.
        success     --> the function called if the request succeeds. It is passed
                        the data returned from the server.
        error       --> the function called if the request fails. It is passed the
                        jqXHR object which can tell us the type of error.

DESCRIPTION

    This Ajax function makes a 'GET' request and is returned back a JsonResponse
    from the ExamDataView() function located inside the "django_project -> Exams
    -> views.py" file.

    The data being managed in the success function is a list of answers
    for each question on an exam.

    In the case of the request succeeding, each element in the list
    is looped through. In the case of an error, the error function
    will output the error to the web console.

    For each element looped through in the list of answers, the question
    and answers are added to the "g_ExamBox" element.

    The innerHTML property sets the HTML content of the "g_ExamBox" element.
    This is important because this generates the format of the exam that a
    user will see.

    The ActivateTimer() function will be passed "response.time". "response"
    is the JsonResponse returned by the ExamDataView() function. "time" is
    the name of the second key inside the Python dictionary that was returned
    with the JsonResponse received from the ExamDataView() function.

    The ActivateTimer() function will take note of the value of "response.time",
    and will begin counting down from that value once the exam has started.

RETURNS

    The purpose of this $.ajax() function is not to return anything, but
    to send a 'GET' request where the accurate set of questions and answers
    for an exam are presented to the exam taker.

*/
$.ajax({
    type: 'GET',
    url: `${g_URL}data`,
    success: function (response) {
        console.log(response);
        const Data = response.data;
        /*Each element has a key and a value. The key represents
          the question and the value represents the answer.
          
          Here each individual element is being grabbed.*/
        Data.forEach(a_element => {
            for (const [question, answers] of Object.entries(a_element)) {
                g_ExamBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `;

                answers.forEach(answer => {
                    g_ExamBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${question}-${answer}"
                                    name="${question}" value="${answer}">
                            <label for="${question}">${answer}</label>
                        </div>
                    `;
                })
            }
        });
        ActivateTimer(response.time);
    },
    error: function (a_error) {
        console.log(a_error);
    }
})
/*$.ajax({ type: 'GET', url: `${g_URL}data`, success: function (response){}, 
           error: function(a_error){} }) */

const g_ScoreBox = document.getElementById('score-box');

const g_ExamForm = document.getElementById('exam-form');

/*I cannot prefix the global variable "csrf" with "g_" or capitalise
  it because this would obstruct the purpose of the variable itself.*/
const csrf = document.getElementsByName('csrfmiddlewaretoken');

const g_ResultBox = document.getElementById('result-box');

/*
SendData = () =>

NAME

    SendData - processes the submission of answers for an
    exam's multiple-choice questions.

SYNOPSIS

    SendData = () =>
        There are no parameters for this function.

DESCRIPTION

    This function will be executed after the event listener below for
    "g_ExamForm" has called the SendData() which occurs when a user
    submits their answers for an exam.
    
    While looping through each element inside the "Elements" list, what
    is verified is whether each element is checked or answered in this
    case. If an element is not checked, it means that a question on an
    exam was not answered, so the element is assigned "null".

    Afterwards, an Ajax function will make a 'POST' request, so that the
    data can be sent to a certain web address. Before the data is sent,
    the success function will indicate whether the test taker has passed
    or not, followed by marking each question as "Correct", "Incorrect",
    or "Not Answered".

RETURNS

    This function does not return anything, but instead makes a 'POST'
    which means that in this instance the exam answers stored inside 
    the "Data" list, will be sent to the URL address assigned to "g_URL".

*/
/*The following function is less than 100 lines.*/
const SendData = () => {
    const Elements = [...document.getElementsByClassName('ans')];
    const Data = {};
    /*Put the csrf middleware token into the "Data" dictionary.*/
    Data['csrfmiddlewaretoken'] = csrf[0].value;

    Elements.forEach(element => {
        if (element.checked)
            Data[element.name] = element.value;

        if (!Data[element.name])
            Data[element.name] = null;
    })

    $.ajax({
        type: 'POST',
        url: `${g_URL}save/`,
        data: Data,
        success: function (response) {
            const Results = response.results;
            console.log(Results);
            g_ExamForm.classList.add('not-visible');

            g_ScoreBox.innerHTML = `${response.passed ? 'Congratulations! ' : 'Pass Unsuccessful: ('}You
                                     scored ${response.score.toFixed(2)}% on the exam.)`;

            Results.forEach(response => {
                const ResDiv = document.createElement("div");

                for (const [Question, Resp] of Object.entries(response)) {
                    console.log(Question);
                    console.log(Resp);
                    console.log('*****');

                    ResDiv.innerHTML += Question;
                    const Cls = ['container', 'p-3', 'text-light', 'h5'];
                    ResDiv.classList.add(...Cls);

                    if (Resp == "not answered") {
                        ResDiv.innerHTML += ' - Not Answered';

                        ResDiv.classList.add('bg-secondary');
                    } else {
                        /*It was necessary to put a nested if statement inside of
                          the else block because this section of code should only
                          be executed if the question on the exam was answered.*/
                        const Answer = Resp['answered'];
                        const Correct = Resp['correctAnswer'];

                        // If the exam taker selected the correct answer.
                        if (Answer == Correct) {
                            ResDiv.classList.add('bg-success');

                            ResDiv.innerHTML += ` Correct | `;
                            ResDiv.innerHTML += `Your Answer: ${Answer}`;
                        } else {
                            // If the exam taker selected an incorrect answer.
                            ResDiv.classList.add('bg-danger');

                            ResDiv.innerHTML += ` Incorrect `;

                            /*Add the text of the correct answer to the HTML
                              element, so that the exam taker can see it.*/
                            ResDiv.innerHTML += ` | Correct Answer: ${Correct}`;
                            ResDiv.innerHTML += ` | Your Answer: ${Answer}`;
                        }
                    }
                }
                g_ResultBox.append(ResDiv);
            })

            g_TimerBox.style.display = "none";
            g_ZeroTimerBox.innerHTML = "<b>00:00</b>";
            g_ZeroTimerBox.style.display = "block";
            console.log("Qakh");
        },
        error: function (a_error) {
            console.log(a_error);
        }
    })
}
/*SendData = () => */


/*
g_ExamForm.addEventListener( =>

NAME

    g_ExamForm.addEventListener - calls the SendData() function when the
    user submits the form containing the exam answers.

SYNOPSIS

    g_ExamForm.addEventListener('submit', a_event =>
        'submit'        --> the event type to listen for.
        a_event         --> the Event interface which represents an
        event taking place in the DOM (Document Object Model).

DESCRIPTION

    This function will be executed when a form containing the answers
    for each multiple-choice question is submitted.

    The preventDefault() method called on the Event interface "a_event"
    will tell the user agent that if the event does not get explicitly
    handled, its default action should not be taken as it normally would
    be.

RETURNS

    Rather than returning anything, this event
    listener will call the SendData() function.

*/
g_ExamForm.addEventListener('submit', a_event => {
    a_event.preventDefault();

    SendData();
})
/*g_ExamForm.addEventListener('submit', a_event => */

/*156*/
