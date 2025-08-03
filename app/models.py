from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt

# Initialize the database instance
db = SQLAlchemy()

class User(db.Model):
    """Defines the User table schema and password handling."""
    
    # Define table columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        """Verifies a password against the stored hash."""
        return bcrypt.verify(password, self.password_hash)

    def to_dict(self):
        """Returns a dictionary representation of the user for JSON responses."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }