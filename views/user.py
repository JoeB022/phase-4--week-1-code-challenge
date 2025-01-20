from flask import jsonify, request, Blueprint,logging
from werkzeug.security import generate_password_hash
from models import db, User

user_bp = Blueprint("user_bp", __name__)

# Fetch all users
@user_bp.route("/users", methods=["GET"])
def fetch_users():
    users = User.query.all()
    user_list = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_approved': user.is_approved,
            'is_admin': user.is_admin,
            'orders': [
                {
                    'id': order.id,
                    'title': order.title,
                    'description': order.description,
                    'deadline': order.deadline,
                    'tag': {
                        'id': order.tag.id if order.tag else None,
                        'name': order.tag.name if order.tag else None
                    }
                }
                for order in user.orders
            ]
        }
        for user in users
    ]
    return jsonify(user_list)

# Add a user
@user_bp.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    is_approved = data.get('is_approved',False)
    is_admin = data.get('is_admin',False)
    password = generate_password_hash(data.get('password'))

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "Username or email already exists"}), 406

    new_user = User(username=username, email=email, password=password,is_approved=is_approved,is_admin=is_admin)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"success": "User added successfully"}), 201

# Update a user
@user_bp.route("/users/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User does not exist"}), 404

    data = request.get_json()
    username = data.get('username', user.username)
    email = data.get('email', user.email)
    password = generate_password_hash(data.get('password')) if data.get('password') else user.password

    if User.query.filter((User.username == username) | (User.email == email), User.id != user.id).first():
        return jsonify({"error": "Username or email already exists"}), 406

    user.username = username
    user.email = email
    user.password = password
    db.session.commit()
    return jsonify({"success": "User updated successfully"}), 200

# Delete a user

@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        # Fetch the user by Id ju nilisemafrom the raote that i will delete by id 
        user = User.query.get(user_id)

        # Check if the user exists..kutoka kwa db
        if not user:
            return jsonify({"error": "User does not exist"}), 404

        # Delete the user
        db.session.delete(user)
        db.session.commit()

        # Success response
        return jsonify({"success": "User deleted successfully"}), 200

    except Exception as e:
        # Log the error for debugging
        logging.error(f"Error deleting user with ID {user_id}: {e}")

        # Return an error response
        return jsonify({"error": "An unexpected error occurred"}), 500