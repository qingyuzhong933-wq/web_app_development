from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.task import Task
from app.models.point_log import PointLog
from datetime import datetime

# 定義任務相關的 Blueprint
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def index():
    """顯示首頁任務清單與總積分"""
    tasks = Task.get_all()
    total_points = PointLog.get_total_points()
    return render_template('index.html', tasks=tasks, total_points=total_points)

@tasks_bp.route('/tasks/add', methods=['POST'])
def add_task():
    """處理新增任務表單提交"""
    title = request.form.get('title')
    points = request.form.get('points', type=int, default=10)
    description = request.form.get('description')
    due_date_str = request.form.get('due_date')
    
    # 基本驗證
    if not title:
        flash('任務標題不可為空！', 'danger')
        return redirect(url_for('tasks.index'))
    
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        except ValueError:
            flash('日期格式錯誤！', 'warning')

    task = Task.create(title=title, points=points, description=description, due_date=due_date)
    if task:
        flash(f'任務 "{title}" 已新增！', 'success')
    else:
        flash('新增任務失敗，請稍後再試。', 'danger')
        
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
def edit_task(id):
    """GET: 顯示編輯頁面; POST: 儲存編輯內容"""
    task = Task.get_by_id(id)
    if not task:
        flash('找不到該任務！', 'danger')
        return redirect(url_for('tasks.index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        points = request.form.get('points', type=int)
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        
        if not title:
            flash('標題不可為空！', 'danger')
            return render_template('edit.html', task=task)
        
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                pass

        if task.update(title=title, points=points, description=description, due_date=due_date):
            flash('任務已更新！', 'success')
            return redirect(url_for('tasks.index'))
        else:
            flash('更新失敗。', 'danger')

    return render_template('edit.html', task=task)

@tasks_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
def toggle_task(id):
    """切換任務完成狀態，並同步更新積分歷程"""
    task = Task.get_by_id(id)
    if not task:
        return redirect(url_for('tasks.index'))
    
    # 切換狀態
    new_status = not task.is_done
    
    # 決定積分變動
    delta = task.points if new_status else -task.points
    reason = f'{"完成" if new_status else "取消"}任務：{task.title}'
    
    if task.update(is_done=new_status):
        PointLog.add_log(task_id=task.id, delta=delta, reason=reason)
        flash(f'積分 {"+" if delta > 0 else ""}{delta}！', 'info')
    
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """刪除指定任務"""
    task = Task.get_by_id(id)
    if task:
        title = task.title
        if task.delete():
            flash(f'任務 "{title}" 已刪除。', 'warning')
        else:
            flash('刪除失敗。', 'danger')
    return redirect(url_for('tasks.index'))
