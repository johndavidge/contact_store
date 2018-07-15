from datetime import timedelta

class Config:
    FLASK_URL = 'http://localhost:5000'
    CELERY_BROKER_URL = 'redis://localhost'
    CELERY_RESULT_BACKEND = 'redis://localhost'
    CELERYBEAT_SCHEDULE = {
        'create-every-15-seconds': {
            'task': 'tasks.create_contact',
            'schedule': timedelta(seconds=15)
        }
    }


    @staticmethod
    def init_app(app):
        pass
