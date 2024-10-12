import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key_here')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/task_management')
    
    # Tăng thời gian hết hạn của token
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=5)  # Ví dụ: token tồn tại trong 1 giờ
