# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from linkage.linking import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.LinkingProjectListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^status/$',
        view=views.AjaxListView.as_view(),
        name='status'
    ),
    url(
        regex=r'^type/$',
        view=views.select_type,
        name='type'
    ),
    url(
        regex=r'^add/(?P<type>[\w.@+-]+)/$',
        view=views.create_project,
        name='add'
    ),
    url(
        regex=r'edit/(?P<type>[\w.@+-]+)/(?P<name>[\w.@+-]+)$',
        view=views.edit_project,
        name='edit'
    ),
    url(
        regex=r'delete/(?P<name>[\w.@+-]+)$',
        view=views.LinkingProjectDeleteView.as_view(),
        name='delete'
    ),
    url(
        regex=r'exec/(?P<name>[\w.@+-]+)$',
        view=views.execute,
        name='exec'
    ),
    url(
        regex=r'results/(?P<name>[\w.@+-]+)$',
        view=views.view_results,
        name='view_results'
    ),
    url(
        regex=r'export/(?P<name>[\w.@+-]+)$',
        view=views.export_to_json,
        name='export'
    ),
    url(
        regex=r'stop/(?P<name>[\w.@+-]+)$',
        view=views.stop_project,
        name='stop_project'
    ),
]
