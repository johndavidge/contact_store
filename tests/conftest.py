import os
import tempfile

import pytest
from contact_store import create_app
from contact_store.database import db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': db_path,
    })

    db.init_app(app)
    with app.app_context():
        from contact_store.models import Contact
        db.create_all()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
