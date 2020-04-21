from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.api.views.thesis import ThesisViewSet

router = DefaultRouter()
router.register(r'thesis', ThesisViewSet)

app_name = 'api'
urlpatterns = [
    path('v1/', include((router.urls, 'v1'))),
]
