# -*- coding: UTF-8 -*-

from django.db import connection


class AuditMiddleware(object):

    def process_request(self, request):
        cursor = connection.cursor()
        cursor.execute('CREATE TEMPORARY TABLE user_tmp (username text)')
        cursor.execute('INSERT INTO "user_tmp" VALUES (%s)', [request.user.username])
