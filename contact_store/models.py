from contact_store.database import db


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    emails = db.relationship('Email', backref='contact', lazy=True)
    first_name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)

    def __init__(self, username, first_name, surname):
        self.username = username
        self.first_name = first_name
        self.surname = surname

    def __repr__(self):
        return '<Contact %r>' % (self.username)

    @property
    def serialize(self):
        return {
            'username':   self.username,
            'emails':     [i.serialize for i in self.emails],
            'first_name': self.first_name,
            'surname':    self.surname,
        }

    @classmethod
    def get_by_email(cls, email):
        return Contact.query.join(Email).filter_by(address=email).first()


class Email(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), unique=True, nullable=False)
    contact_id = db.Column(db.Integer,
                           db.ForeignKey('contacts.id'),
                           nullable=False)

    def __init__(self, address):
        self.address = address

    def __repr__(self):
        return '<Email %r>' % (self.address)

    @property
    def serialize(self):
        return {
            'address': self.address,
        }
