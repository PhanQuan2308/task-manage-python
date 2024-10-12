from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from routes.auth_routes import auth_bp
from routes.task_routes import task_bp

app = Flask(__name__)
app.config.from_object(Config)

# Bật CORS và JWT
CORS(app)
jwt = JWTManager(app)

# Đăng ký các blueprint
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(task_bp, url_prefix="/tasks")

if __name__ == "__main__":
    app.run(debug=False)
