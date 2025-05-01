/* The JavaScript in this file is responsible
   for presenting the details linked to each
	 specific exam within the modal box popup. */

const g_ModalBtns = [...document.getElementsByClassName('modal-button')];

const g_Exams = document.querySelector('.exams');

/*
g_ModalBtns.forEach(
	a_modalBtn => a_modalBtn.addEventListener('click', () =>

NAME

	g_ModalBtns.forEach(
		a_modalBtn => a_modalBtn.addEventListener -
		monitors each button for click events.

SYNOPSIS

	g_ModalBtns.forEach(
		a_modalBtn => a_modalBtn.addEventListener('click', () =>

		a_modalBtn        --> the single button which this
		function will observe in order to wait for a 'click'
		event to occur.
		'click'           --> the click event where a user
		clicks on the button which triggers the code inside
		of the addEventListener() method to be executed.

DESCRIPTION

	This function will grab each button by grabbing
	a single "a_modalBtn".

	It will then retrieve all of the attributes
	associated with a button listed for an "Exam"
	object inside "django_project/Exams/templates/main.html".

	In other words, each button is being grabbed from
	an array and will be listened to on a 'click' event.

	Some of the attributes associated with the button,
	are then included in a text section where the
	difficulty, number of questions, score required to
	pass, and time limit is displayed to the user before
	they take an exam.

RETURNS

	Nothing is returned by this function, but by
	grabbing the 'start-btn' element element and
	getting the URL of the current page, the user
	will be directed to a web page where they will
	see questions for the exam they have chosen to take.

*/
g_ModalBtns.forEach(
	a_modalBtn => a_modalBtn.addEventListener('click', () => {
    const Pk = a_modalBtn.getAttribute('data-pk');
    const Name = a_modalBtn.getAttribute('data-quiz');
    const NumQuestions = a_modalBtn.getAttribute('data-questions');
    const Difficulty = a_modalBtn.getAttribute('data-difficulty');
    const ScoreToPass = a_modalBtn.getAttribute('data-pass');
    const Time = a_modalBtn.getAttribute('data-time');

    const ModalBody = document.getElementById('modal-body-confirm');

		/* h1 is the largest boostrap heading
		   class while h6 is the smallest.

			 mb-3 adds margin-bottom spacing. */
    ModalBody.innerHTML = `
			<div class="h3 mb-3">
				Are you confident that you would like
				to start the "<b>${Name}</b>" exam?
			</div>

			<div class="text-muted">
				<ul>
					<li>Difficulty level: <b>${Difficulty}</b></li>
					<li>Amount of questions: <b>${NumQuestions}</b></li>
					<li>Required score to pass: <b>${ScoreToPass}%</b></li>
					<li>Time limit: <b>${Time} min</b></li>
				</ul>
			</div>

			<button type="button" id="start-button"
				class="btn btn-success">
				Yes
			</button>

			<button type="button" class="btn btn-danger"
				data-dismiss="modal">
				No
			</button>
    `;

    const StartBtn = document.getElementById('start-button');

    const URL = window.location.href;

		g_Exams.classList.toggle('hidden');

    /* When executing the following code, ensure that
		   the DOM (Document Object Model) element is found
			 before calling an addEventListener() method on it.
       In this case, 'g_StartBtn' is the DOM element. */
    StartBtn.addEventListener('click', () => {
			console.log('URL', URL);
			console.log('Pk:', Pk);
      window.location.href = URL + Pk;
    })
}))
/*g_ModalBtns.forEach(
	a_modalBtn => a_modalBtn.addEventListener('click', () => */

/* 27 */