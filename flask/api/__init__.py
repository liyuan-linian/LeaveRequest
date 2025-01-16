from flask import Blueprint

api_blueprint = Blueprint('api', __name__)

# 引入其他模块
from . import Model, Auth, users
