from flask import Flask, jsonify, request, flash, url_for, redirect, \
                  render_template

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('contact_store.cfg')
db = SQLAlchemy(app)


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)

    @property
    def serialize(self):
        return {
            'username'   : self.username,
            'email'      : self.email,
            'first_name' : self.first_name,
            'surname'    : self.surname,
        }


def get_contact(username):
    return Contact.query.filter_by(username=username).first()

@app.route('/contacts', methods=['GET'])
def list_contacts():
    if request.method == 'GET':
        return jsonify(contacts=[i.serialize for i in Contact.query.all()])


@app.route('/contacts/<username>', methods=['GET'])
def show_contact(username):
    contact = get_contact(username)

    if contact is not None:
        return jsonify(contact.serialize)
    else:
        content = 'A contact with username: %s could not be found.' % username
        return content, 404


@app.route('/contacts/<username>', methods=['PUT'])
def update_contact(username):
    if request.method == 'PUT':
        contact = get_contact(username)

        if contact is not None:
            if not request.is_json:
                return 'Invalid JSON', 400
            data = request.get_json()

            new_username = data['username']
            new_email = data['email']
            new_first_name = data['first_name']
            new_surname = data['surname']

            updates = False
            if new_username is not None:
                updates = True
                contact.username = new_username
            if new_email is not None:
                updates = True
                contact.email = new_email
            if new_first_name is not None:
                updates = True
                contact.first_name = new_first_name
            if new_surname is not None:
                updates = True
                contact.surname = new_surname
            
            if updates:
                try:
                    db.session.commit()
                except:
                    content = 'Error inserting values into DB.'
                    return content, 400

                content = 'Contact: %s updated sucessfully.' % contact.username
                return content

            content = 'Contact: %s not updated. No new data given.'
            return content, 400
        else:
            content = 'A contact with username: %s could not be found.' % username
            return content, 404


@app.route('/contacts/<username>', methods=['DELETE'])
def delete_contact(username):
    contact = get_contact(username)

    if contact is not None:
        try:
            db.session.delete(contact)
            db.session.commit()
        except:
            content = 'Error attempting to delete contact: %s' % username
            return content, 400

        content = 'Contact: %s deleted sucessfully.' % username
        return content

    content = 'A contact with username: %s could not be found.' % username
    return content, 404


@app.route('/contacts', methods=['POST'])
def create_contact():
    if request.method == 'POST':
        if not request.is_json:
            return 'Invalid JSON', 400
        data = request.get_json()

        username = data['username']
        email = data['email']
        first_name = data['first_name']
        surname = data['surname']

        error = None
        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not first_name:
            error = 'First name is required.'
        elif not surname:
            error = 'Surname is required.'

        if error is None:
            try:
                new_contact = Contact(username=username,
                                      email=email,
                                      first_name=first_name,
                                      surname=surname)
                db.session.add(new_contact)
                db.session.commit()
            except:
                content = 'Error inserting values into DB.'
                return content, 400
            content = 'New contact: %s, created successfully.' % username
            return content

        return error, 400


if __name__ == '__main__':
    db.create_all()
    app.run()
