from datetime import datetime

from app import db_user
from flask import g, request, jsonify

from . import api_blueprint
from .Auth import role_required
from .Model import Leave_request


# 其中个人的信息从g.user中可以得到 该请求需要参数为 levae_start_time leave_end_time leave_reason leave_location leave_alternative apply_time获取系统时间
@api_blueprint.route("/create_new_request", methods=["POST"])
@role_required('user')
def create_new_request():
    leave_start_time = request.json.get('leave_start_time')
    leave_end_time = request.json.get('leave_end_time')
    leave_reason = request.json.get('leave_reason')
    leave_location = request.json.get('leave_location')
    leave_alternative = request.json.get('leave_alternative')

    leave_start_time = datetime.strptime(leave_start_time, '%Y-%m-%d %H:%M:%S')
    leave_end_time = datetime.strptime(leave_end_time, '%Y-%m-%d %H:%M:%S')

    leave_request = Leave_request(
        user_id=g.user.id,
        leave_start_time=leave_start_time,
        leave_end_time=leave_end_time,
        leave_reason=leave_reason,
        leave_location=leave_location,
        leave_alternative=leave_alternative,
        apply_time=datetime.now(),
        status="submitted"
    )

    db_user.session.add(leave_request)

    try:
        db_user.session.commit()
    except Exception as e:
        db_user.session.rollback()
        return jsonify({"message": "error", "Error": str(e)})

    return jsonify({"message": "success"}), 201

# 用于领导审批
@api_blueprint.route("/leave_request/approve/<int:id>", methods=["POST"])
@role_required('leader')
def leave_request(id):
    action = request.json.get('action')
    message = request.json.get('message')

    leave_request = Leave_request.query.filter_by(id=id).first()

    if not leave_request:
        return jsonify({"message": "error", "Error": "No such request"}),404

    if leave_request.status != "submitted":
        return jsonify({"message": "error", "Error": "该请求无需审批"}), 400

    if action == 1:
        leave_request.approve(message=message)
    if action == 0:
        leave_request.reject(message=message)
    else:
        return jsonify({"message": "error","Error":"bad action"}), 400

    try:
        db_user.session.commit()
    except Exception as e:
        db_user.session.rollback()
        return jsonify({"message": "error", "Error": str(e)})

    return jsonify({"message": "success"}), 200

#重新提交申请
@api_blueprint.route("/leave_request/re_submitt/<int:id>", methods=["POST"])
@role_required('user')
def leave_request_re_submitted(id):
    leave_request = Leave_request.query.filter_by(id=id).first()

    if not leave_request:
        return jsonify({"message": "error", "Error": "No such request"}),404
    if leave_request.status == "submitted":
        return jsonify({"message":"error","Error":"this request is  to be submitted"}), 400

    leave_request.status = "submitted"
    try:
        db_user.session.commit()
    except Exception as e:
        db_user.session.rollback()
        return jsonify({"message": "error", "Error": str(e)}), 400

    return jsonify({"message": "success"}), 200

# 条件查找 使用例子
# GET /leave_requests?user_id=1&status=submitted
# GET /leave_requests?leave_start=2025-01-01 00:00:00&leave_end=2025-01-31 23:59:59
# GET /leave_requests?reason=vacation
@api_blueprint.route("/leave_request/user", methods=["GET"])
@role_required('user')
def get_leave_requests_user():
    #userid 配合user中get_userinfo 接口使用 前端先从另接口获取当前用户信息 再来get该接口

    user_id = request.json.get('user_id')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    alternative = request.json.get('alternative')
    status = request.json.get('status')

    query = Leave_request.query

    if user_id:
        query = query.filter(Leave_request.user_id == user_id)

    if status:
        query = query.filter(Leave_request.status == status)

    if start_time:
        try:
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            query = query.filter(Leave_request.start_time >= start_time)
        except ValueError:
            return jsonify({"message":"error","ERROR":"error format"})

    if end_time:
        try:
            end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            query = query.filter(Leave_request.end_time <= end_time)
        except ValueError:
            return jsonify({"message":"error","ERROR":"error format"})

    if alternative:
        query = query.filter(Leave_request.alternative == alternative)

    leave_requests = query.all()

    result = [{
        "id": leave_request.id,
        "user_id": leave_request.user_id,
        "start_time": leave_request.start_time,
        "end_time": leave_request.end_time,
        "reason": leave_request.reason,
        "alternative": leave_request.alternative,
        "status": leave_request.status,
        "message": leave_request.message,
        "apply_time": leave_request.apply_time,
        "location": leave_request.location,
    }for leave_request in leave_requests]

    return jsonify(result),200

