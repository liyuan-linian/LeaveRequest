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
    levae_start_time = request.json.get('levae_start_time')
    leave_end_time = request.json.get('leave_end_time')
    leave_reason = request.json.get('leave_reason')
    leave_location = request.json.get('leave_location')
    leave_alternative = request.json.get('leave_alternative')

    levae_start_time = datetime.strptime(levae_start_time, '%Y-%m-%d %H:%M:%S')
    leave_end_time = datetime.strptime(leave_end_time, '%Y-%m-%d %H:%M:%S')

    leave_request = Leave_request(
        user_id=g.user.id,
        levae_start_time=levae_start_time,
        leave_end_time=leave_end_time,
        leave_reason=leave_reason,
        leave_location=leave_location,
        leave_alternative=leave_alternative,
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


# 条件查找 使用例子 领导权限可以任意查询  user权限需要验证g.user
# GET /leave_requests?user_id=1&status=submitted
# GET /leave_requests?leave_start=2025-01-01 00:00:00&leave_end=2025-01-31 23:59:59
# GET /leave_requests?reason=vacation
@api_blueprint.route("/leave_request/user", methods=["GET"])
@role_required('user')
def get_leave_requests_user():
    user_id = request.json.get('user_id')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    reason = request.json.get('reason')
    alternative = request.json.get('alternative')
    status = request.json.get('status')

    query = Leave_request.query


