from flask import Blueprint, request, jsonify
from .models import db, User
# You will also need to create these files later
# from .schemas import UserCreate, UserUpdate
# from .services import create_jwt_token

# A Blueprint is a way to organize a group of related views and other code.
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def health_check():
    return jsonify({"status": "healthy"}), 200

@main_bp.route('/users', methods=['GET'])
def get_users():
    """Gets all users from the database."""
    users = User.query.all()
    # Use the to_dict() method to create a list of user dictionaries
    return jsonify([user.to_dict() for user in users]), 200

@main_bp.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    """Gets a single user by their ID."""
    # .get_or_404 is a shortcut to get a user or return a 404 Not Found error
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict()), 200

@main_bp.route('/users', methods=['POST'])
def create_user():
    """Creates a new user."""
    data = request.get_json()
    if not data or not data.get('email') or not data.get('name') or not data.get('password'):
        return jsonify({"error": "Missing data"}), 400

    # Check if a user with that email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email address already in use"}), 409 # 409 Conflict

    # Create a new User instance
    new_user = User(
        name=data['name'],
        email=data['email']
    )
    # Use the set_password method to hash the password
    new_user.set_password(data['password'])
    
    # Add to the database
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(new_user.to_dict()), 201 # 201 Created

@main_bp.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    """Updates an existing user."""
    user = User.query.get_or_404(id)
    data = request.get_json()

    # Update fields if they are provided in the request
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    
    db.session.commit()
    return jsonify(user.to_dict()), 200

@main_bp.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    """Deletes a user."""
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

@main_bp.route('/search', methods=['GET'])
def search_users():
    """Searches for users by name."""
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Name query parameter is required"}), 400
    
    # Use .ilike() for a case-insensitive search
    users = User.query.filter(User.name.ilike(f'%{name}%')).all()
    return jsonify([user.to_dict() for user in users]), 200

@main_bp.route('/login', methods=['POST'])
def login():
    """Logs a user in by verifying their credentials."""
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=data['email']).first()

    # Use the check_password method to securely verify the password
    if user and user.check_password(data['password']):
        # In a real app, you would generate a JWT token here
        return jsonify({"message": "Login successful", "user": user.to_dict()}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401 # 401 Unauthorized