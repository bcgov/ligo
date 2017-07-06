# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from linkage.datasets import views

urlpatterns = [
    url(
        regex=r'^preview/$',
        view=views.dataset_preview,
        name='get_preview'
    ),
    url(
        regex=r'^header/$',
        view=views.dataset_header,
        name='header'
    ),
    url(
        regex=r'^$',
        view=views.DatasetListView.as_view(),
        name='list'
    ),
    url(
        regex=r'add/$',
        view=views.DatasetCreateView.as_view(),
        name='add'
    ),
    url(
        regex=r'edit/(?P<name>[\w.@+-]+)/$',
        view=views.DatasetUpdateView.as_view(),
        name='edit'
    ),
    url(
        regex=r'delete/(?P<name>[\w.@+-]+)/$',
        view=views.DatasetDeleteView.as_view(),
        name='delete'
    ),
    url(
        regex=r'^(?P<name>[\w.@+-]+)/$',
        view=views.DatasetDetailView.as_view(),
        name='detail'
    ),
 ]
