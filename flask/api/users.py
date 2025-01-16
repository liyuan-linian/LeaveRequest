from app import db_user
from flask import request, abort, jsonify, g

from . import api_blueprint
from .Auth import auth, role_required
from .Model import User


# 普通用户注册
@api_blueprint.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    department = request.json.get('department')
    phone_num_long = request.json.get('phone_num_long')
    phone_num_short = request.json.get('phone_num_short')
    email = request.json.get('email')
    position = request.json.get('position')

    # 验证信息
    if username is None or password is None:
        abort(400, "输入信息有误")
    if User.query.filter_by(username=username).first() is not None:
        abort(400, 'User already exists')  # 用户名已存在

    user = User(
        username=username,
        department=department,
        phone_num_long=phone_num_long,
        phone_num_short=phone_num_short,
        email=email,
        position=position
    )

    user.hash_password(password)

    db_user.session.add(user)
    db_user.session.commit()

    # 这里可以返回更多信息
    return jsonify({'username': user.username})


@api_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return jsonify({"message": "Invalid username or password"}), 401

    token = user.generate_auth_token(expiration=3600)
    # 根据需要返回需要的用户信息
    return jsonify({
        'token': token
    })


@api_blueprint.route('/userinfo/<string:username>', methods=['GET'])
@role_required(role="user")
def get_userinfo(username):
    if g.user.username != username:
        abort(403)

    user = User.query.filter_by(username=username).first()
    if not user:
        abort(400)

    # 可以返回更多信息
    # 姓名 用户基本信息等 请假记录
    return jsonify(
        {
            'username': user.username,
            'department': user.department,
            'phone_num_long': user.phone_num_long,
            'phone_num_short': user.phone_num_short,
            'email': user.email,
            'positon': user.positon
        }
    )

#修改个人信息界面




#测试页面
@api_blueprint.route('/test/admin', methods=['GET'])
@role_required(role="admin")
def admin():
    return jsonify({"message": "admin"})


@api_blueprint.route('/test/leader', methods=['GET'])
@role_required(role="leader")
def leader():
    return jsonify({"message": "leader"})


@api_blueprint.route('/test/user', methods=['GET'])
@role_required(role="user")
def user():
    return jsonify({"message": "user"})