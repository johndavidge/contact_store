import os

from contact_store import create_app
from contact_store.tasks import celery

app = create_app()
app.app_context().push()
