from django.db import models
import random

# This file contains the definitions
# for the models of the "Exams" app.

DIFF_CHOICES = (
	('Easy', 'Easy'),
	('Medium', 'Medium'),
	('Challenging', 'Challenging')
)


class Exam(models.Model):
	m_examName = models.CharField(
		max_length=120, verbose_name='Exam Name')

	m_material = models.CharField(
		max_length=120, verbose_name='Material')

	m_questionCount = models.IntegerField(
		verbose_name="Question Count")

	m_timeLimit = models.IntegerField(
		help_text="duration of the exam in minutes",
		verbose_name='Time Limit')

	m_scoreRequiredToPass = models.IntegerField(
		help_text="required score in %",
		verbose_name='Score Required To Pass')

	m_difficulty = models.CharField(
		max_length=11, choices=DIFF_CHOICES,
		verbose_name='Difficulty')

	def __str__(self):
		return f"{self.m_examName}: {self.m_material}"

	def GetExamQuestions(self):
		# "ExamQuestion" is the model in ExamQuestions/models.py
		# where the questions are being grabbed from.
		questions = list(self.question_set.all())

		# random.shuffle(questions) will re-order the
		# questions for each exam, so that they don't
		# appear in the same order every time.
		random.shuffle(questions)

		# [:self.question_count] ensures that the amount
		# of questions received will be limited to the
		# number of question there are for an exam.
		return questions[:self.m_questionCount]

	class Meta:
		verbose_name = "Exam"
		verbose_name_plural = 'Exams'

# 26