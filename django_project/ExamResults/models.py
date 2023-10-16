from django.db import models

# This file contains the definitions for the models of the "ExamResults" app.

from Exams.models import Exam
from django.contrib.auth.models import User


class Result(models.Model):
    m_exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="Exam")
    m_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    m_examScore = models.FloatField(verbose_name="Exam Score")

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Exam Result"
        verbose_name_plural = "Exam Results"

# 11
