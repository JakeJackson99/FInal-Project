"""The various models required by the system.

The program needs to store various information, such as its users (for the
dashboard), and the behaviours exhibited on the experiment page. Here, the
models for such data is set out.
"""

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login


@login.user_loader
def load_user(id):
    """Required by Flask-Login to allow for sessions.

    Args:
        id: The id of the user being tested.

    Returns:
        The id of the user.
    """
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    """Represents a user, i.e. the admin user.

    Args:
        db.Model: Inherates from Flask-SQLAlchemy.
        UserMixin: Inherates from Flask-Login.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """Turn the user's inputted password into a hash value and sets it.

        Args:
            password: The user's password to be hashed.
        """

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the inputted password matches the stored hash of the user.

        Args:
            password: A password to be hashed and checked against.
        """
        return check_password_hash(self.password_hash, password)


class UserBehaviours(db.Model):
    """Represents user behaviours.

    Args:
        db.Model: Inherates from Flask-SQLAlchemy
    """

    id = db.Column(db.Integer, primary_key=True)
    endless = db.Column(db.Boolean, nullable=False)
    time_seconds = db.Column(db.Integer)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(8))

    def __repr__(self):
        return '<id: {}, endless: {}, time: {}>'.format(self.id, self.endless,
                                                        self.time_seconds)
