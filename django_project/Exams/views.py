from django.shortcuts import render
from .models import Exam
from django.views.generic import ListView
from django.http import JsonResponse
from ExamQuestions.models import Question, Answer
from ExamResults.models import Result

# The view functions in this file handle the
# POST and GET requests for the "Exams"
# application.


class ExamListView(ListView):
  model = Exam
  template_name = 'Exams/main.html'


"""
ExamView()

NAME

  ExamView - handles the HttpRequest to the 'exams/<pk>/' address.

SYNOPSIS

	def ExamView(request, pk):
		request        --> the HttpRequest object which
    Django uses to pass state through the system.
		pk             --> the primary key which is
    necessary for finding a particular "Exam" object.

DESCRIPTION

	This function will accept a web request, assign a
  certain "Exam" object linked to the primary key
  accepted as a parameter called "pk", to a variable
	called "exam", and will then return a web response.

	It takes the HttpRequest object which is one its
  parameters, and returns it while rendering the HTML
  template titled 'exam.html' along with sending a 
	key-value pair, so that the HTML template has access
  to it.

RETURNS

	Returns an HttpResponse object while directing the
  user to the 'exam.html' template located inside the
  "Exams" application.

	A particular "Exam" object that corresponds to the
  primary key parameter is sent to the HTML template
  as a key named "obj".

"""


def ExamView(request, pk):
	exam = Exam.objects.get(pk=pk)

	# Assign the exam value to 'obj', and
	# then send it to the exam.html template.
	return render(request, 'Exams/exam.html', {'obj': exam})
# def ExamView(request, pk):

'''
"request" must be included as a parameter or else
when taking an exam, there will be an error message
saying the following:

TypeError: ExamDataView() got multiple values for argument 'pk'
'''


"""
ExamDataView()

NAME

  ExamDataView - handles the HttpRequest to the
  'exams/<pk>/data/' address.

SYNOPSIS

	def ExamDataView(request, pk):
		request        --> the HttpRequest object which
		Django uses to pass
		state through the system.
		pk             --> the primary key which is necessary
		for finding a particular "Exam" object.

DESCRIPTION

	This function will accept a web request, assign a
	certain "Exam" object linked to the primary key
	accepted as a parameter called "pk", to a variable
	called "exam".

	The questions and answers for that particular "Exam"
	object are added to two separate empty lists called
	"questions" and "answers".

	It takes the HttpRequest object which is one its
	parameters, and returns it while rendering the HTML
	template titled 'exam.html' along with sending a 
	key-value pair, so that the HTML template has access
	to it.

RETURNS

	Returns a JsonResponse object containing the
	"questions" Python list sent as a key-value
  pair with the key having the name "data".

	The time limit for the "Exam" object is likewise
  sent as a key-value pair with the key having the
  name "time".

"""


def ExamDataView(request, pk):
	exam = Exam.objects.get(pk=pk)
	questions = []

	for question in exam.GetExamQuestions():
		answers = []

		for answer in question.GetExamAnswers():
			answers.append(answer.m_text)

		questions.append({str(question): answers})

	return JsonResponse({
		'data': questions,
		'time': exam.m_timeLimit
	})
# def ExamDataView(request, pk):


"""
is_ajax()

NAME

	is_ajax - handles the HttpRequest to the
  'exams/<pk>/data/' address.

	In this views.py file, the SaveExamView() is the
  only functon where the is_ajax() function is called.

SYNOPSIS

	def is_ajax(request):
		request        --> the HttpRequest object which
    Django uses to pass state through the system.

DESCRIPTION

	This function will accept a web request, assign a
  certain "Exam" object linked to the primary key
  accepted as a parameter called "pk", to a variable
	called "exam".

	This function will accept a web request, and will
  then return an HTTP_X_REQUESTED_WITH header with the
  value of the header being equal to 'XMLHttpRequest'.

RETURNS

	Returns an HTTP_X_REQUESTED_WITH header which is sent
	together with a request that must be announced as an
  AJAX request.

"""


def is_ajax(request):
  return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
# def is_ajax(request):

# 'pk' always stands for "primary key".
# The primary key represents the exam that is
# currently being accepted as an argument.


"""
SaveExamView()

NAME

  SaveExamView - handles the HttpRequest
  to the 'exams/<pk>/data/' address.

SYNOPSIS

	def SaveExamView(request, pk):
		request        --> the HttpRequest object which
    Django uses to pass state through the system.
		pk             --> the primary key which is
    necessary for finding a particular "Exam" object.

DESCRIPTION

	If an AJAX request is accepted, the data from the
  POST request is extracted and used to generate a
  dictionary named "data_".

	The 'csrfmiddlewaretoken' is removed from the
  dictionary "data_".

	The keys in the "data_" dictionary are the questions
  of an exam that are then used to assign the questions
  to an "questions" list.

	The user who sent the POST request, and the "Exam"
  object that corresponds to the primary key "pk" are
  both retrieved.

	The "examScore" is set to zero while the user's
  score is calculated based on whether they answered
  each question correctly.

RETURNS

	If the score the user received ("score_") is greater
  than or equal to the score required to pass, a
  JsonResponse object returned with "passed" having the
  value of "True" is returned.

	Otherwise, if the user did not pass, a JsonResponse
  object with "passed" having the value of "False" is
  returned.

"""


def SaveExamView(request, pk):
	'''
	A nested if statement was needed here because
	the following section of code should only be
	executed if this view function has received
	an AJAX request.'''
	if is_ajax(request):
		data = request.POST
		data_ = dict(data.lists())
		data_.pop('csrfmiddlewaretoken')
		questions = []

		# The keys are the questions.
		for key in data_.keys():
			# print('key:', key)

			question = Question.objects.get(m_text=key)
			questions.append(question)

		# print(questions)

		user = request.user
		exam = Exam.objects.get(pk=pk)

		examScore = 0
		multiplier = 100 / exam.m_questionCount
		results = []
		correctAnswer = None

		'''
		Nested for loop where I looped through each
		question, and then within the for loop, I
		looped through the possible answers for that
		particular question.'''
		for question in questions:
			a_selected = request.POST.get(question.m_text)

			# If the answer selected by the
			# exam taker was not left blank.
			if a_selected != "":
				questionAnswers = Answer.objects.filter(m_question=question)

				for answer in questionAnswers:
					'''
					A nested if statement was necessary here because
					even if the answer selected by the user was incorrect,
					I still needed to find the correct multiple choice
					answer for the question inside of the else block.

					I accomplished this by making sure that when
					"answer.m_text" held the correct multiple choice
					answer for the question, "answer.m_correct" would
					be equal to true. In the iteration where this is
					occuring, "answer.m_text" is assigned to "correctAnswer".

					Check if the the answer selected by the exam taker is
					equal to one of the answers in "questionAnswers", and
					is furthermore, correct.

					"a_selected" is the multiple choice answer selected by
					the exam taker.

					"answer.m_text" will show one multiple choice answer
					on each iteration. A total of four are looped through
					for a particular question.

					"answer.m_correct" will hold a boolean value. When the
					correct "answer.m_text" (multiple choice answer) is
					looped through, the value of "answer.m_correct" will
					be true.

					All of the four multiple choice answers for each
					question will be looped through, and compared to
					the answer chosen by the user.'''
					if a_selected == answer.m_text and answer.m_correct:
						print("\nCorrect answer chosen.")
						print("a_selected:", a_selected)
						print("answer.m_text:", answer.m_text)
						print("answer.m_correct:", answer.m_correct)

						# If the question was answered
						# correctly, increase the score.
						examScore += 1
						correctAnswer = answer.m_text
					else:
						print("\nWrong answer chosen.")
						print("a_selected:", a_selected)
						print("answer.m_text:", answer.m_text)
						print("answer.m_correct:", answer.m_correct)

						'''
						If an exam taker selects the wrong multiple choice
						answer, the correct answer will still be found.
						
						When "answer.m_correct" is equal to true, it indicates
						that "answer.m_text" is holding the correct multiple
						choice answer for this specific question.'''
						if answer.m_correct:
							correctAnswer = answer.m_text

				results.append(
					{str(question):
						{'correctAnswer': correctAnswer, 'answered': a_selected}})
			else:
				results.append({str(question): 'not answered'})

		score_ = examScore * multiplier

		Result.objects.create(m_exam=exam, m_user=user, m_examScore=score_)

		if score_ >= exam.m_scoreRequiredToPass:
			return JsonResponse(
				{'passed': True, 'score': score_, 'results': results})
		else:
			return JsonResponse(
				{'passed': False, 'score': score_, 'results': results})
# def SaveExamView(request, pk):

# 68