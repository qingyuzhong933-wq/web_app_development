from datetime import datetime
from app.models import db

class Task(db.Model):
    """
    任務模型 (Task Model)
    負責儲存使用者建立的待辦事項資訊。
    """
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    points = db.Column(db.Integer, default=10)
    is_done = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Task {self.title}>'

    @classmethod
    def get_all(cls):
        """取得所有任務，依建立時間倒序排列"""
        try:
            return cls.query.order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error getting all tasks: {e}")
            return []

    @classmethod
    def get_by_id(cls, task_id):
        """根據 ID 取得單筆任務"""
        try:
            return cls.query.get(task_id)
        except Exception as e:
            print(f"Error getting task by id {task_id}: {e}")
            return None

    @classmethod
    def create(cls, title, points=10, description=None, due_date=None):
        """
        建立新任務
        :param title: 任務標題 (必填)
        :param points: 積分 (預設 10)
        :param description: 描述 (選填)
        :param due_date: 截止日期 (選填)
        """
        try:
            new_task = cls(
                title=title,
                points=points,
                description=description,
                due_date=due_date
            )
            db.session.add(new_task)
            db.session.commit()
            return new_task
        except Exception as e:
            db.session.rollback()
            print(f"Error creating task: {e}")
            return None

    def update(self, title=None, points=None, description=None, due_date=None, is_done=None):
        """
        更新現有任務資訊
        """
        try:
            if title is not None: self.title = title
            if points is not None: self.points = points
            if description is not None: self.description = description
            if due_date is not None: self.due_date = due_date
            if is_done is not None: self.is_done = is_done
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating task {self.id}: {e}")
            return False

    def delete(self):
        """
        刪除任務
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting task {self.id}: {e}")
            return False
