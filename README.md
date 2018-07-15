# contact_store
A simple Flask app for storing and retrieving contact information.

Makes use of Celery to automatically create and delete example contacts.

## Setup

_**These instructions assume you are using a linux-based system. Some commands may differ for other systems.
Refer to the relevant project documentation where necessary.**_

Clone and cd into the project repo:

```
$ git clone https://github.com/johndavidge/contact_store.git
$ cd contact_store
```

Create and activate a virtual environment:

```
$ python3 -m venv venv
$ . venv/bin/activate
```

Install the required packages:

```
$ pip install -r requirements.txt
```

This app also requires the use of redis-server to support the celery message broker.
If you don't already have it you can install it from your favourite package manager, e.g:

```
# apt-get install redis-server
```

If it isn't already, run the redis-server:

```
$ redis-server
```

Set the following Flask environment variables:

```
$ export FLASK_APP=contact_store
$ export FLASK_ENV=development
```

Before running the app, you can verify that everything is setup correctly by running the tests:

```
$ pytest
======================================== test session starts ========================================
platform linux -- Python 3.6.5, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: /home/john/contact_store, inifile: setup.cfg
plugins: celery-4.2.0
collected 7 items                                                                                   

tests/test_contacts.py ......                                                                 [ 85%]
tests/test_factory.py .                                                                       [100%]

===================================== 7 passed in 0.32 seconds ======================================
```

## Running the Flask app

To run the app, use:

```
$ flask run
```

## Running the Celery worker

The flask app will have hijacked your current terminal window, so open another one, navigate to the contact_store directory and activate the virtual environment as before. Then run:

```
$ celery worker -A celery_worker.celery -l info -E -B
```

The `-B` option starts the celery beat service within the worker, scheduling periodic tasks without the need for a separate worker.

## Watching it work

Now open a browser and navigate to:

```http://localhost:5000/contacts```

You should see a JSON representation of all contacts currently stored.

The celery worker will add a new randomly generated contact every 15 seconds.

It will also delete each new contact 60 seconds after it was created.

You'll need to refresh your browser to see this happening.

## API Reference

The contact_store API supports getting, creating, updating, and deleting of contacts in the following JSON format:

```
{
  'username'   : 'test_contact',
  'emails'     : [
                   {'address' : 'test@contact.com'},
                   {'address' : 'contact@test.com'}
                 ],
  'first_name' : 'Test',
  'surname'    : 'Contact',
}
```

You can interact with the API at the following endpoints:

### /contacts

_GET - Returns a JSON formatted list of all stored contacts._

_POST - Accepts a JSON formatted contact and stores it (if valid)._

### /contacts/<username_or_email>

_GET** - Returns a JSON formatted contact if it exists._

_PUT - Updates a stored contact if it exists._

_DELETE - Deletes a stored contact if it exists._
