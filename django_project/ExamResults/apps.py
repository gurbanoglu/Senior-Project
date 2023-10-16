from django.apps import AppConfig

# This file includes application configuration for
# the "ExamResults" app by configuring its attributes.


class ExamResultsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ExamResults'

    # The following changes the name of the application's
    # title displayed on the admin page.
    verbose_name = 'EXAM RESULTS'

# 5
