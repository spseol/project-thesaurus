from django.urls import path

from apps.thesis.views import ThesisCreateView

app_name = 'thesis'
urlpatterns = [
    path('create/', ThesisCreateView.as_view()),
]
