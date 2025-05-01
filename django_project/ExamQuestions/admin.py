from django.contrib import admin
from .models import Question, Answer

# The models for the "ExamQuestions" app
# are registered here.


class AnswerInline(admin.TabularInline):
  model = Answer


class QuestionAdmin(admin.ModelAdmin):
  inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)

# 7