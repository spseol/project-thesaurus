# -*- coding: UTF-8 -*-
from django.conf.urls import url

from olc.audit.views import HistoryView

urlpatterns = [

    url(r"^form/history/(?P<tables>[\w\-]+)/(?P<keyName>[\w\-]+)/(?P<keyValue>[\w\-]+)/$", HistoryView.as_view(),
        name="history_form"),

]
