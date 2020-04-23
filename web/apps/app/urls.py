from django.urls import re_path

from apps.app.views import AppView

urlpatterns = [
    re_path('.*', AppView.as_view()),
]
