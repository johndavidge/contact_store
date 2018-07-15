from flask import Blueprint, jsonify, request

from contact_store.database import db
from contact_store.models import Contact
from contact_store.models import Email

bp = Blueprint('contacts', __name__, url_prefix='/contacts')


def get_contact(username_or_email):
    contact = Contact.query.filter_by(username=username_or_email).first()

    if contact is not None:
        return contact

    return Contact.get_by_email(username_or_email)


@bp.route('', methods=['GET'])
def list_contacts():
    if request.method == 'GET':
        return jsonify(contacts=[i.serialize for i in Contact.query.all()])


@bp.route('/<username_or_email>', methods=['GET'])
def show_contact(username_or_email):
    contact = get_contact(username_or_email)

    if contact is not None:
        return jsonify(contact.serialize)
    else:
        content = ('A contact with username or email: '
                   '%s could not be found.' % username_or_email)
        return content, 404


@bp.route('/<username>', methods=['PUT'])
def update_contact(username):
    if request.method == 'PUT':
        contact = get_contact(username)

        if contact is None:
            content = ('A contact with username: '
                       '%s could not be found.' % username)
            return content, 404

        if not request.is_json:
            return 'Invalid JSON', 400
        data = request.get_json()

        new_username = None
        new_emails = None
        new_first_name = None
        new_surname = None

        if 'username' in data:
            new_username = data['username']
        if 'emails' in data:
            new_emails = data['emails']
        if 'first_name' in data:
            new_first_name = data['first_name']
        if 'surname' in data:
            new_surname = data['surname']

        updates = False
        if new_username is not None:
            updates = True
            contact.username = new_username
        if new_emails is not None:
            updates = True
            for email in contact.emails:
                db.session.delete(email)
            for email in new_emails:
                new_email = Email(address=email['address'])
                db.session.add(new_email)
                contact.emails.append(new_email)
        if new_first_name is not None:
            updates = True
            contact.first_name = new_first_name
        if new_surname is not None:
            updates = True
            contact.surname = new_surname

        if updates:
            try:
                db.session.commit()
            except Exception:
                content = 'Error inserting values into DB.'
                return content, 500

            content = 'Contact: %s updated sucessfully.' % contact.username
            return content

        content = ('Contact: %s not updated. '
                   'No new data given.' % contact.username)
        return content, 400


@bp.route('/<username>', methods=['DELETE'])
def delete_contact(username):
    contact = get_contact(username)

    if contact is not None:
        try:
            for email in contact.emails:
                db.session.delete(email)
            db.session.delete(contact)
            db.session.commit()
        except Exception:
            content = 'Error attempting to delete contact: %s' % username
            return content, 500

        content = 'Contact: %s deleted sucessfully.' % username
        return content

    content = 'A contact with username: %s could not be found.' % username
    return content, 404


@bp.route('', methods=['POST'])
def create_contact():
    if request.method == 'POST':
        if not request.is_json:
            return 'Invalid JSON', 400
        data = request.get_json()

        print(data)

        error = None
        if 'username' not in data or not data['username']:
            error = 'Username is required.'
        elif 'emails' not in data or not data['emails']:
            error = 'Email is required.'
        elif 'first_name' not in data or not data['first_name']:
            error = 'First name is required.'
        elif 'surname' not in data or not data['surname']:
            error = 'Surname is required.'

        if error is None:
            username = data['username']
            emails = data['emails']
            first_name = data['first_name']
            surname = data['surname']
            try:
                new_contact = Contact(username=username,
                                      first_name=first_name,
                                      surname=surname)
                for address in emails:
                    new_email = Email(address=address['address'])
                    db.session.add(new_email)
                    new_contact.emails.append(new_email)
                db.session.add(new_contact)
                db.session.commit()
            except Exception:
                content = 'Error inserting values into DB.'
                return content, 500
            content = 'New contact: %s, created successfully.' % username
            return content

        return error, 400
