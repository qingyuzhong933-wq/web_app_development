from flask import Blueprint, render_template
from app.models.point_log import PointLog

# 定義積分相關的 Blueprint
points_bp = Blueprint('points', __name__)

@points_bp.route('/points/log')
def log():
    """顯示積分變動歷程清單"""
    pass
