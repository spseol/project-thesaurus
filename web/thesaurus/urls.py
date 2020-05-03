"""thesaurus URL Configuration"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from loginas.views import user_logout

from apps.frontend.views import AppView

urlpatterns = [
    path('admin/', include('loginas.urls')),
    path('admin/', admin.site.urls, name='admin'),

    path('api/', include('apps.api.urls')),
]

urlpatterns += i18n_patterns(
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', user_logout, name='logout'),
    re_path('.*', AppView.as_view(), name='home'),
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),

                  ] + urlpatterns
