import os
import logging
from celery import Celery
from cdilinker.linker.commands import execute_project
from cdilinker.linker.algorithms import get_algorithms
from cdilinker.linker.base import FIELD_CATEGORIES

logger = logging.getLogger(__name__)


env = os.environ

BROKER_URL = env.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
RESULT_BACKEND = env.get('CELERY_BROKER_URL', 'redis://redis:6379/0')


app = Celery('linkage', backend=RESULT_BACKEND, brocker=BROKER_URL)

@app.task(name="linkage.run_project")
def run_task(name, project_json):

    logger.debug("name : {0}".format(name))
    logger.info("Starting project: {0}".format(name))
    logger.debug("project_json : {0}".format(project_json))
    report_file = execute_project(project_json)
    logger.debug("report_file : {0}".format(report_file))

    return report_file


@app.task(name="linkage.algorithms")
def linkage_algorithms():

    algorithms = {}

    tsf_alg = get_algorithms(types=['TSF'])
    dtr_alg = get_algorithms(types=['DTR', None])
    prb_alg = get_algorithms(types=['PRB', None])

    blocking = tuple((k, v.title) for k, v in tsf_alg.items())
    linking = {
        'DTR': tuple((k, v.title) for k, v in dtr_alg.items()),
        'PRB': tuple((k, v.title) for k, v in prb_alg.items())
    }
    args = {
        'DTR': dict((k, v.args) for k, v in dtr_alg.items()),
        'PRB': dict((k, v.args) for k, v in prb_alg.items())
    }

    algorithms['blocking'] = blocking
    algorithms['linking'] = linking
    algorithms['args'] = args

    return algorithms


@app.task(name="linkage.field_categories")
def linkage_field_categories():

    field_cats = tuple((item.name, item.title) for item in FIELD_CATEGORIES)

    return field_cats
