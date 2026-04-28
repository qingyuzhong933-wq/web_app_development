from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.task import Task
from app.models.point_log import PointLog

# 定義任務相關的 Blueprint
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def index():
    """顯示首頁任務清單"""
    pass

@tasks_bp.route('/tasks/add', methods=['POST'])
def add_task():
    """處理新增任務表單提交"""
    pass

@tasks_bp.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
def edit_task(id):
    """GET: 顯示編輯頁面; POST: 儲存編輯內容"""
    pass

@tasks_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
def toggle_task(id):
    """切換任務完成狀態，並同步更新積分歷程"""
    pass

@tasks_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """刪除指定任務"""
    pass
