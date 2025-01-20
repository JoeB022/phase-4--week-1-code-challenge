from flask import jsonify, request, Blueprint
from models import db, User
from werkzeug.security import check_password_hash
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt,unset_jwt_cookies
from werkzeug.security import generate_password_hash

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Query user by email
    user = User.query.filter(User.email == email).first()

    if user and check_password_hash(user.password, password):
        # Correctly generate the access token
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

    #ccurrent use
@auth_bp.route("/current_user", methods=["GET"])
@jwt_required()
def current_user():
    current_user_id  = get_jwt_identity()

    user = User.query.get(current_user_id)
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_approved": user.is_approved,
        "is_admin": user.is_admin
    }
    return jsonify(user_data)

# user update
@auth_bp.route("/user/<int:user_id>", methods=["PATCH"])
@jwt_required()
def update_user(user_id):
    # here is now getting the curret user Id from the jwt requesttoken
    current_user_id = get_jwt_identity()
    if current_user_id!= user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if "name"in data:
        user.name = data['name']
    if "email" in data:
        user.email = data['email']
    if "password" in data:
        user.password = generate_password_hash(data['password'])

    
    db.session.commit()
    return jsonify({"success": "User profile updated successfully"}), 200

# Helper function for hashing password (if you don't have it)
def hash_password(password):
    return generate_password_hash(password)

# update password
@auth_bp.route("/user/<int:user_id>/password", methods=["PUT"])
@jwt_required()
def update_password(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id!= user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    old_password = data['old_password']
    new_password = data['new_password']

    if not check_password_hash(user.password, old_password):
        return jsonify({"error": "Invalid old password"}), 401

    user.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({"success": "Password updated successfully"}), 200


# Logout
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    logedout = jsonify({"text":"logedout success"})
    unset_jwt_cookies(logedout)
    return logedout



