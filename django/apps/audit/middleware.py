# -*- coding: UTF-8 -*-

from django.db import connection
from django.utils.deprecation import MiddlewareMixin


class AuditMiddleware(MiddlewareMixin):
    """
    Has to be placed after Django AuthMiddleware.
    """

    def process_request(self, request):
        cursor = connection.cursor()
        # alternative https://www.postgresql.org/docs/9.6/functions-admin.html
        cursor.execute('CREATE TEMPORARY TABLE IF NOT EXISTS _user_tmp (user_id integer);')
        cursor.execute('INSERT INTO "_user_tmp" VALUES (%s);', [request.user.id or None])

    def process_response(self, request, response):
        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS _user_tmp;')
        return response
