from app import db_user
from flask import request, abort, jsonify, g

from . import api_blueprint
from .Auth import role_required
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


# 修改个人信息界面,不包括密码
@api_blueprint.route('/update_userinfo', methods=['PUT'])
@role_required(role="user")
def update_userinfo():
    user = g.user
    data = request.get_json()

    if data is None:
        return jsonify({"message": "没有提供数据"})

    allowed_fields = ['username', 'department', 'phone_num_long', 'phone_num_short', "email", "position"]
    updated_fields = []
    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])
            updated_fields[field] = data[field]

    if not updated_fields:
        return jsonify({"message": "No date to update"})

    try:
        db_user.session.commit()
    except Exception as e:
        db_user.session.rollback()
        return jsonify({"message": "error", "Error": str(e)})

    return jsonify({
        "message": "success",
        "data": updated_fields
    }), 200


# 通过该api 可以使用用户的user_name查询到用户的id 需要解决的问题是同名用户的id返回问题
# 用户名可能存在重复  可以采用电话短号的方式进行查询
@api_blueprint.route('/get_user_id', methods=['GET'])
@role_required(role="admin")
def get_user_id():
    num = request.json.get('phone_num_short')

    if not num:
        return jsonify({"message": "Num is required"})

    user = User.query.filter_by(phone_num_short=num).first()

    if not user:
        return jsonify({"message": "user not found"})

    return jsonify({
        "username": user.username,
        "id": user.id
    })


# 管理员修改其他人的信息和密码
@api_blueprint.route('/api/update_userinfo/<int:user_id>', methods=['PUT'])
@role_required(role="admin")
def update_userinfo0(user_id):
    user = User.query.get(user_id)

    data = request.get_json()

    if data is None:
        return jsonify({"message": "没有提供数据"})

    allowed_fields = ['username', 'department', 'phone_num_long', 'phone_num_short', "email", "position"]
    updated_fields = []
    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])
            updated_fields[field] = data[field]

    if not updated_fields:
        return jsonify({"message": "No date to update"})

    try:
        db_user.session.commit()
    except Exception as e:
        db_user.session.rollback()
        return jsonify({"message": "error", "Error": str(e)})

    return jsonify({
        "message": "success",
        "data": updated_fields
    }), 200


# 修改密码
@api_blueprint.route('/update_password', methods=['POST'])
@role_required(role="user")
def update_password():
    user = g.user
    new_password = request.json.get('new_password')

    if new_password is None:
        return jsonify({"message": "no new password"})

    user.hash_password(new_password)
    try:
        db_user.session.commit()
    except Exception as e:
        db_user.session.rollback()
        return jsonify({"message": "error", "Error": str(e)})

    return jsonify({
        "message": "success",
        "new_password": new_password
    })


@api_blueprint.route('/update_password/<int:user_id>', methods=['PUT'])
@role_required(role="admin")
def update_password0(user_id):
    user = User.query.get(user_id)
    new_password = request.json.get('new_password')

    if new_password is None:
        return jsonify({"message": "no new password"})

    user.hash_password(new_password)
    try:
        db_user.session.commit()
    except Exception as e:
        db_user.session.rollback()
        return jsonify({"message": "error", "Error": str(e)})

    return jsonify({
        "message": "success",
        "new_password": new_password
    })


# 测试页面
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
