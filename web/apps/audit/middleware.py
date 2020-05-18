# -*- coding: UTF-8 -*-

from django.db import connection
from django.utils.deprecation import MiddlewareMixin


class AuditMiddleware(MiddlewareMixin):
    """
    Has to be placed after Django AuthMiddleware.
    """

    def process_request(self, request):
        cursor = connection.cursor()
        cursor.execute('CREATE TEMPORARY TABLE _user_tmp (username text)')
        cursor.execute('INSERT INTO "_user_tmp" VALUES (%s)', [request.user.username])
