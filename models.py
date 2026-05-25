from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Volunteer(db.Model):
    __tablename__ = 'volunteer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))
    year_of_study = db.Column(db.Integer)
    skills = db.Column(db.Text)

    assignments = db.relationship('Assignment', backref='volunteer', lazy=True,
                                  cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Volunteer {self.name}>'


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='volunteer')
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    volunteer = db.relationship(
        'Volunteer',
        backref=db.backref('user_account', uselist=False),
        lazy=True
    )

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Club(db.Model):
    __tablename__ = 'club'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    coordinator_name = db.Column(db.String(100))

    events = db.relationship('Event', backref='club', lazy=True,
                             cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Club {self.name}>'


class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)

    assignments = db.relationship('Assignment', backref='event', lazy=True,
                                  cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Event {self.name}>'


class Assignment(db.Model):
    __tablename__ = 'assignment'

    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    hours_logged = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='pending')   # 'pending' | 'completed'

    def __repr__(self):
        return f'<Assignment vol={self.volunteer_id} evt={self.event_id}>'
