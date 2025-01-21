import time
from datetime import datetime

import jwt
from app import db_user
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash


class User(db_user.Model):
    __tablename__ = 'users'
    id = db_user.Column(db_user.Integer, primary_key=True)
    username = db_user.Column(db_user.String(64), nullable=False, index=True)
    password_Hash = db_user.Column(db_user.String(64), nullable=False)
    role = db_user.Column(db_user.String(64), default="user")  # admin  leader user
    # token生成需要字符串 因此讲权限换成string类型
    department = db_user.Column(db_user.String(64), nullable=False)
    phone_num_long = db_user.Column(db_user.String(64), nullable=False)
    phone_num_short = db_user.Column(db_user.String(32), nullable=False)
    email = db_user.Column(db_user.String(64), nullable=False)
    position = db_user.Column(db_user.String(64), nullable=False)
    leave_request = db_user.relationship('Leave_request', backref='user', lazy=True)

    def __init__(self, username, department, phone_num_long, phone_num_short, email, position):
        self.username = username
        # self.password_Hash = generate_password_hash(password)
        self.role = "user"  # 默认查看
        self.department = department
        self.phone_num_long = phone_num_long
        self.phone_num_short = phone_num_short
        self.email = email
        self.position = position

    def hash_password(self, password):
        self.password_Hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_Hash, password)

    def generate_auth_token(self, expiration=600):
        return jwt.encode(
            {'username': self.username, 'role': self.role, 'exp': time.time() + expiration},
            Config.SECRET_KEY, algorithm='HS256'
        )

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return None
        return User.query.get(data['id'])


class Leave_request(db_user.Model):
    __tablename__ = 'leave_requests'
    id = db_user.Column(db_user.Integer, primary_key=True)
    user_id = db_user.Column(db_user.Integer, db_user.ForeignKey('users.id'), nullable=False)
    apply_time = db_user.Column(db_user.DateTime, default=datetime.now())
    levae_start_time = db_user.Column(db_user.DateTime)
    leave_end_time = db_user.Column(db_user.DateTime)
    leave_reason = db_user.Column(db_user.String(200), nullable=False)
    leave_location = db_user.Column(db_user.String(200), nullable=False)
    leave_alternative = db_user.Column(db_user.String(200), nullable=False)
    status = db_user.Column(db_user.String(200), nullable=False)
    message = db_user.Column(db_user.String(200), nullable=False,default='无')

    def __init__(self, user_id, apply_time,leave_start_time,leave_reason,leave_end_time, leave_location, leave_alternative,status="submitted"):
        self.user_id = user_id
        self.apply_time = apply_time
        self.levae_start_time = leave_start_time
        self.leave_end_time = leave_end_time
        self.leave_location = leave_location
        self.leave_alternative = leave_alternative
        self.leave_reason = leave_reason
        self.status = status

    def approve(self,message):
        self.status = "approved"
        if self.message :
            self.message = message

    def reject(self,message):
        self.status = "rejected"
        if self.message :
            self.message = message
