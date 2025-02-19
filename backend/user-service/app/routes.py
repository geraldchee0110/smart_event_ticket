from flask import Blueprint, request, jsonify
from app import supabase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint("users", __name__)

# 📌 User Registration (Hash password before storing)
@user_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if "username" not in data or "email" not in data or "password" not in data:
            return jsonify({"error": "Missing username, email, or password"}), 400

        # ✅ Hash the password before storing
        hashed_password = generate_password_hash(data["password"])

        # ✅ Insert user into Supabase
        response = supabase.table("users").insert({
            "username": data["username"],
            "email": data["email"],
            "password_hash": hashed_password  # Ensure column exists in Supabase
        }).execute()

        if isinstance(response, dict) and "error" in response:
            return jsonify({"error": response["error"]["message"]}), 400

        return jsonify({"message": "User registered successfully", "data": response.data}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 📌 User Login (Compare hashed password)
@user_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if "email" not in data or "password" not in data:
            return jsonify({"error": "Missing email or password"}), 400

        # ✅ Fetch user from Supabase
        response = supabase.table("users").select("*").eq("email", data["email"]).execute()

        if not response.data:
            return jsonify({"error": "Invalid email or password"}), 401

        user = response.data[0]  # Get first user record

        # ✅ Compare hashed password
        if not check_password_hash(user["password_hash"], data["password"]):
            return jsonify({"error": "Invalid email or password"}), 401

        # ✅ Generate JWT Token
        access_token = create_access_token(identity=user["email"])
        return jsonify(access_token=access_token), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@user_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": "Access granted", "user": current_user}), 200
def broken_function():
print("This should fail linting")  # 🚨 Incorrect indentation