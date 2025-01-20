from flask import jsonify, request, Blueprint
from models import db, Order
from datetime import datetime


Order_bp = Blueprint("order_bp", __name__)

# CREATE
@Order_bp.route("/orders", methods=["POST"])
def add_order():
    order_request = request.get_json()

    if not order_request:
        return jsonify({"error": "No order data provided"}), 400

    try:
        user_id = order_request["user_id"]

        # Convert `order_date` to a datetime.date object
        order_date = order_request.get("order_date", None)
        if order_date:
            order_date = datetime.strptime(order_date, "%Y-%m-%d").date()
        else:
            order_date = datetime.now().date()  # Default to today's date

        total_amount = order_request["total_amount"]
        order_status = order_request.get("order_status", "Pending")

        # Create the new order
        new_order = Order(
            user_id=user_id,
            order_date=order_date,
            total_amount=total_amount,
            order_status=order_status
        )
        db.session.add(new_order)
        db.session.commit()

        return jsonify({
            "success": "Order added successfully",
            "order": {
                "id": new_order.id,
                "user_id": new_order.user_id,
                "order_date": new_order.order_date.isoformat(),  # Convert back to string for JSON response
                "total_amount": new_order.total_amount,
                "order_status": new_order.order_status
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to add order", "details": str(e)}), 500

# READ ALL
@Order_bp.route("/orders", methods=["GET"])
def get_all_orders():
    orders = Order.query.all()
    order_list = [{
        "id": order.id,
        "user_id": order.user_id,
        "order_date": order.order_date,
        "total_amount": order.total_amount,
        "order_status": order.order_status
    } for order in orders]
    return jsonify({"orders": order_list}), 200


# READ SINGLE
@Order_bp.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = Order.query.get(order_id)
    if order:
        return jsonify({"order": {
            "id": order.id,
            "user_id": order.user_id,
            "order_date": order.order_date,
            "total_amount": order.total_amount,
            "order_status": order.order_status
        }}), 200
    else:
        return jsonify({"error": "Order not found"}), 404


# UPDATE
@Order_bp.route("/orders/<int:order_id>", methods=["PATCH"])
def update_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    order_request = request.get_json()
    if not order_request:
        return jsonify({"error": "No data provided"}), 400

    try:
        order.user_id = order_request.get("user_id", order.user_id)
        order.total_amount = order_request.get("total_amount", order.total_amount)
        order.order_status = order_request.get("order_status", order.order_status)

        db.session.commit()
        return jsonify({"success": "Order updated successfully", "order": {
            "id": order.id,
            "user_id": order.user_id,
            "order_date": order.order_date,
            "total_amount": order.total_amount,
            "order_status": order.order_status
        }}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update order", "details": str(e)}), 500


# DELETE
@Order_bp.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if order:
        try:
            db.session.delete(order)
            db.session.commit()
            return jsonify({"success": "Order deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Failed to delete order", "details": str(e)}), 500
    else:
        return jsonify({"error": "Order not found"}), 404
