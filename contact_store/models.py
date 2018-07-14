from contact_store.database import db


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)

    def __init__(self, username, email, first_name, surname):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.surname = surname

    def __repr__(self):
        return '<Contact %r>' % (self.username)

    @property
    def serialize(self):
        return {
            'username'   : self.username,
            'email'      : self.email,
            'first_name' : self.first_name,
            'surname'    : self.surname,
        }

