from flask import Blueprint, jsonify, request
from models import Product,db
Product_bp = Blueprint("Product_bp", __name__)

# Add a new product
@Product_bp.route("/product", methods=["POST"])
def add_product():
    product_request = request.get_json()

    if not product_request:
        return jsonify({"error": "No product data provided"}), 400

    try:
        name = product_request["name"]
        category = product_request["category"]
        description = product_request["description"]
        price = product_request["price"]

        # Support both 'stock_quantity' and 'stock_quality'
        stock_quantity = product_request.get("stock_quantity")
        if not stock_quantity:  # If 'stock_quantity' is not provided, check 'stock_quality'
            stock_quantity = product_request.get("stock_quality")
            if stock_quantity is None:  # Both are missing
                return jsonify({"error": "Missing field: 'stock_quantity' or 'stock_quality'"}), 400

        # Validate stock_quantity is an integer
        if not isinstance(stock_quantity, int):
            return jsonify({"error": "'stock_quantity' must be an integer"}), 400

        image_url = product_request["image_url"]

        new_product = Product(
            name=name,
            category=category,
            description=description,
            price=price,
            stock_quantity=stock_quantity,
            image_url=image_url
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({
            "success": "Product added successfully",
            "product": {
                "id": new_product.id,
                "name": new_product.name,
                "category": new_product.category,
                "description": new_product.description,
                "price": new_product.price,
                "stock_quantity": new_product.stock_quantity,
                "image_url": new_product.image_url
            }
        }), 201

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to add product", "details": str(e)}), 500


# Get all products
@Product_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([
        {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "description": product.description,
            "price": product.price,
            "stock_quantity": product.stock_quantity,
            "image_url": product.image_url
        }
        for product in products
    ])

# Update a product
@Product_bp.route("/products/<string:product_name>", methods=["PATCH"])
def update_product(product_name):
    product = Product.query.filter_by(name=product_name).first()
    if not product:
        return jsonify({"error": "Product not found in store"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    product.name = data.get("name", product.name)
    product.category = data.get("category", product.category)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.stock_quantity = data.get("stock_quantity", product.stock_quantity)
    product.image_url = data.get("image_url", product.image_url)

    try:
        db.session.commit()
        return jsonify({
            "success": "Product updated successfully",
            "product": {
                "id": product.id,
                "name": product.name,
                "category": product.category,
                "description": product.description,
                "price": product.price,
                "stock_quantity": product.stock_quantity,
                "image_url": product.image_url
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update product", "details": str(e)}), 500

# Delete a product
@Product_bp.route('/product/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        try:
            db.session.delete(product)
            db.session.commit()
            return jsonify({"success": "Product deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Failed to delete product", "details": str(e)}), 500
    else:
        return jsonify({"error": "Product not found"}), 404
