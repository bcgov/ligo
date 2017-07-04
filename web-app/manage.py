#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    #it is for celery; not appropriate for prod use
    #either create a user with less privilege
    #or use this settings to make sure celery can run
    os.environ.setdefault('C_FORCE_ROOT', 'true')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as e:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python.
        try:
            import django  # noqa
        except ImportError as err:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
