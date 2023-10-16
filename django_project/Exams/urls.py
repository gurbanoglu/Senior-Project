from django.urls import path

# The URL patterns here enable navigation throughout the web pages defined in the "Exams" app.

from .views import (
    ExamListView,
    ExamView,
    ExamDataView,
    SaveExamView,
)

# It was necessary to include “app_name” in this urls.py file for the
# "Exams" application because it contains a namespace.

# I could not make the global variable "app_name" prefixed with "g_"
# because doing so would obstruct the purpose of the variable itself.
app_name = 'Exams'

urlpatterns = [
    path('exams/', ExamListView.as_view(), name='view-exams'),

    # Grab the primary key that was entered in the address bar.
    path('exams/<pk>/', ExamView, name='exam-view'),
    path('exams/<pk>/save/', SaveExamView, name='save-view'),
    path('exams/<pk>/data/', ExamDataView, name='exam-data-view'),
]

# 13
