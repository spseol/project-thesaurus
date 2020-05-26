"""thesaurus URL Configuration"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.staticfiles.urls import urlpatterns as static_urlpatterns
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from loginas.views import user_logout

from apps.frontend.views import AppView

handler500 = 'apps.utils.views.server_error'

urlpatterns = [
    path('api/', include('apps.api.urls')),
]

urlpatterns += i18n_patterns(
    path('admin/', include('loginas.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('login', views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout', user_logout, name='logout'),
    re_path('.*', AppView.as_view(), name='home'),
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      *static_urlpatterns,
                      path('__debug__/', include(debug_toolbar.urls)),
                      # path('400', TemplateView.as_view(template_name='400.html')),
                      # path('403', TemplateView.as_view(template_name='403.html')),
                      # path('404', TemplateView.as_view(template_name='404.html')),
                      path('500', TemplateView.as_view(template_name='500.html')),
                  ] + urlpatterns
