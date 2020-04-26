from django.urls import path, include
from django.utils import timezone
from django.views.decorators.http import last_modified
from django.views.i18n import JSONCatalog
from rest_framework.routers import DefaultRouter

from apps.api.views.category import CategoryOptionsViewSet
from apps.api.views.login import LoginView
from apps.api.views.reservation import ReservationViewSet
from apps.api.views.thesis import ThesisViewSet
from apps.api.views.user import UserOptionsViewSet, StudentOptionsViewSet, TeacherOptionsViewSet

last_modified_date = timezone.now()

router = DefaultRouter()
router.register(r'thesis', ThesisViewSet)
router.register(r'reservation', ReservationViewSet)
router.register(r'user-options', UserOptionsViewSet)
router.register(r'student-options', StudentOptionsViewSet)
router.register(r'teacher-options', TeacherOptionsViewSet)
router.register(r'category-options', CategoryOptionsViewSet)

app_name = 'api'
urlpatterns = [
    path('v1/', include((router.urls, 'v1'))),
    path('v1/login', LoginView.as_view()),

    path('i18n/catalog', last_modified(lambda req, **kw: last_modified_date)(JSONCatalog.as_view(domain='django'))),
    path('i18n/', include('django.conf.urls.i18n')),

]
