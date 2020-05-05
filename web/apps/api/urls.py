from django.urls import path, include
from django.utils import timezone
from django.views.decorators.http import last_modified
from django.views.i18n import JSONCatalog
from rest_framework.routers import DefaultRouter

from .views.attachment import AttachmentViewSet
from .views.category import CategoryOptionsViewSet
from .views.dashboard import DashboardView
from .views.login import LoginView
from .views.reservation import ReservationViewSet
from .views.review import ReviewViewSet
from .views.thesis import ThesisViewSet
from .views.user import UserFilterOptionsViewSet, StudentOptionsViewSet, TeacherOptionsViewSet, UserPermView

last_modified_date = timezone.now()

router = DefaultRouter(trailing_slash=False)
router.register(r'thesis', ThesisViewSet)
router.register(r'reservation', ReservationViewSet)
router.register(r'attachment', AttachmentViewSet)
router.register(r'review', ReviewViewSet)

router.register(r'user-filter-options', UserFilterOptionsViewSet, basename='user')
router.register(r'student-options', StudentOptionsViewSet, basename='student')
router.register(r'teacher-options', TeacherOptionsViewSet, basename='teacher')
router.register(r'category-options', CategoryOptionsViewSet)

app_name = 'api'
urlpatterns = [
    path('v1/', include((router.urls, 'v1'))),
    path('v1/login', LoginView.as_view()),
    path('v1/dashboard', DashboardView.as_view()),
    path('v1/has-perm/<str:perm>', UserPermView.as_view(), name='has-perm'),

    path('i18n/catalog', last_modified(lambda req, **kw: last_modified_date)(JSONCatalog.as_view(domain='django'))),
    path('i18n/', include('django.conf.urls.i18n')),

]
