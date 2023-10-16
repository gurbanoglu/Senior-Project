from django.db import models
from Exams.models import Exam

# This file contains the definitions for the models of the "ExamQuestions" app.


class Question(models.Model):
    m_text = models.CharField(max_length=220, verbose_name="Question")
    m_exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="Exam")
    m_created = models.DateTimeField(auto_now_add=True, verbose_name="Created")

    def __str__(self):
        return str(self.m_text)

    def GetExamAnswers(self):
        return self.answer_set.all()

    class Meta:
        verbose_name = "Exam Question"
        verbose_name_plural = "Exam Questions"


class Answer(models.Model):
    m_text = models.CharField(max_length=220, verbose_name="Answer")
    m_correct = models.BooleanField(default=False, verbose_name="Correct")
    m_question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Question")
    m_created = models.DateTimeField(auto_now_add=True, verbose_name="Created")

    def __str__(self):
        return f"Question: {self.m_question.m_text}, answer: {self.m_text}, correct: {self.m_correct}"

    class Meta:
        verbose_name = "Exam Answer"
        verbose_name_plural = "Exam Answers"

# 20
