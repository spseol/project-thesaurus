from typing import Optional

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import url_has_allowed_host_and_scheme
from funcy import project
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    REDIRECT_FIELD_NAME = 'next'

    error_messages = AuthenticationForm.error_messages

    def post(self, request: Request):
        """
        Performs login through Django authentication system.
        :param request:
        :param format:
        :return:
        """
        user: Optional[User] = authenticate(request=request._request, **project(request.data, ('username', 'password')))
        if user and user.is_active:
            login(request=request._request, user=user)
            return Response(
                data=dict(success=True),
                status=status.HTTP_202_ACCEPTED,
                headers={'Location': self.get_redirect_url() or settings.LOGIN_REDIRECT_URL}
            )
        elif user and not user.is_active:
            return Response(
                data=dict(success=False, message=self.error_messages['inactive']),
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(
            data=dict(
                success=False,
                message=self.error_messages['invalid_login'] % dict(username=User._meta.get_field(
                    User.USERNAME_FIELD
                ).verbose_name)
            ),
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.data.get(self.REDIRECT_FIELD_NAME)
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.request._request.get_host(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''
