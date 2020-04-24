from django.urls import path, include
from django.views import i18n
from rest_framework.routers import DefaultRouter

from apps.api.views.category import CategoryViewSet
from apps.api.views.login import LoginView
from apps.api.views.thesis import ThesisViewSet
from apps.api.views.user import UserOptionsViewSet

router = DefaultRouter()
router.register(r'thesis', ThesisViewSet)
router.register(r'teacher', UserOptionsViewSet)
router.register(r'category', CategoryViewSet)

app_name = 'api'
urlpatterns = [
    path('v1/', include((router.urls, 'v1'))),
    path('v1/login', LoginView.as_view()),

    # TODO: add vue-i18n with data from this view
    path('i18n/', i18n.JSONCatalog.as_view(domain='django')),
]
