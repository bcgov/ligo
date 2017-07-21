import os
import json
import logging

from django.shortcuts import render
from linkage.taskapp.tasks import linkage_linklib_info
from django.conf import settings

logger = logging.getLogger(__name__)

linkapp_info = linkage_linklib_info()


def get_source_commit():

    logger.info('ROOT_DIR: {0}, APP_DIR: {1}'.format(settings.ROOT_DIR, settings.APPS_DIR))

    source_commit_file = os.path.join(settings.ROOT_DIR(), 'git_commits.json')

    try:
        with open(source_commit_file) as commit_file:
            return json.load(commit_file)

    except OSError:
        return dict()



def about_view(request):

    logger.info('Application about page.')
    git_commits = get_source_commit()
    data = {
        'app_version': settings.APP_VERSION,
        'link_version': linkapp_info.get('version'),
        'web_commit': git_commits.get('web_source_commit', ''),
        'link_commit': git_commits.get('link_source_commit', '')
    }

    return render(request, 'pages/about.html', {'data': data})

