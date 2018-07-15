import names
import requests

from celery import Celery
from config import Config

celery = Celery(__name__,
                broker=Config.CELERY_BROKER_URL,
                backend=Config.CELERY_RESULT_BACKEND)


def make_celery(app):
    celery.conf.update(app.config)
    celery.conf.beat_schedule = Config.CELERYBEAT_SCHEDULE

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask


@celery.task(name='tasks.create_contact')
def create_contact():
    request_url = Config.FLASK_URL + '/contacts'
    first_name = names.get_first_name()
    surname = names.get_last_name()
    username = first_name + surname
    email1 = first_name + '@' + surname + '.com'
    email2 = surname + '@' + first_name + '.com'
    contact = {
            'username'   : username,
            'emails'     : [
                    {'address' : email1},
                    {'address' : email2}
                ],
            'first_name' : first_name,
            'surname'    : surname,
        }

    result = requests.post(request_url, json=contact)
    if result.status_code == 200:
        delete_contact.apply_async((username,), countdown=60)


@celery.task(name='tasks.delete_contact')
def delete_contact(username_or_email, *args):
    request_url = Config.FLASK_URL + '/contacts/' + username_or_email
    requests.delete(request_url)
