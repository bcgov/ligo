import logging

from celery.result import AsyncResult
from linkage.taskapp.celery import app

logger = logging.getLogger(__name__)


class TaskStatus:
    PENDING = 'Pending'
    DONE = 'Done'
    FAILED = 'Failed'


def run_task(name, project_json):
    logger.info('Creating a task for the project {0} and adding it to the queue.'.format(name))
    task = app.send_task('linkage.run_project', args=[name, project_json], kwargs={})

    return task


def get_task_result(task_id):
    """
    Tracks a running task by task id and returns the results if it is ready.
    :param task_id: The id of the running task.
    :return: The results if the task is completed.
    """
    try:
        task = AsyncResult(task_id)
        if task.ready():
            result = task.get(timeout=1)

            logger.info("Results are ready for task {0}.".format(task_id))
            logger.info(result)
            return TaskStatus.DONE, result
        else:
            return TaskStatus.PENDING, None

    except Exception:
        return TaskStatus.FAILED, None


def stop_task(task_id):

    AsyncResult(task_id).revoke(terminate=True)


def linkage_algorithms():
    logger.info('Getting the list of comparison algorithms.')
    task = app.send_task('linkage.algorithms', args=[], kwargs={})

    algorithms = task.get()
    return algorithms


def linkage_field_categories():

    logger.info('Getting the list of field categories.')
    task = app.send_task('linkage.field_categories', args=[], kwargs={})

    field_cats = task.get()
    return field_cats


def linkage_linklib_info():

    logger.info('Getting linking library metadata')
    task = app.send_task('linkage.linklib_info', args=[], kwargs={})

    linklib_info = task.get()

    return linklib_info
