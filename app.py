from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import User, Product, Order , db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta



# Initialize app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db.init_app(app)


# import all functions in views
#used this to import all the files that are in the views flder
from views import Product_bp,Order_bp,user_bp,auth_bp

# /JWT -EXTENDED for Flask ..
app.config["JWT_SECRET_KEY"] = "jdfbjbcdhurhfjxbnm " 
# //limit the token of authorizationa dn how long it shiuld take to expire !
app.config["JWT_ACCESS_TOKEN_EXPIRE"] = timedelta(hours = 20)
jwt = JWTManager(app)
jwt.init_app(app)

# Register blueprints here
app.register_blueprint(user_bp)
app.register_blueprint(Product_bp)
app.register_blueprint(Order_bp)
app.register_blueprint(auth_bp)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)