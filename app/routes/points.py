from flask import Blueprint, render_template
from app.models.point_log import PointLog

# 定義積分相關的 Blueprint
points_bp = Blueprint('points', __name__)

@points_bp.route('/points/log')
def log():
    """顯示積分變動歷程清單"""
    logs = PointLog.get_all()
    total_points = PointLog.get_total_points()
    return render_template('point_log.html', logs=logs, total_points=total_points)
