"""thesaurus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('', include('apps.home.urls')),
    path('thesis/', include('apps.thesis.urls')),

    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),

    # since DRF CoreAPI does not support namespacing :-(
    path('api/docs/', include_docs_urls(title='Thesaurus API'), name='api-docs'),
    path('api/', include('apps.api.urls')),

    path('admin/', admin.site.urls),
]

if settings.DEBUG and not urlpatterns:
    urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),

                  ] + urlpatterns
