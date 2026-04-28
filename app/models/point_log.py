from datetime import datetime
from app.models import db

class PointLog(db.Model):
    __tablename__ = 'point_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, nullable=True)  # 關聯任務 ID，設為 nullable 以防任務刪除
    delta = db.Column(db.Integer, nullable=False)   # 積分變動值 (+/-)
    reason = db.Column(db.String(200), nullable=True) # 變動原因 (任務標題)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<PointLog {self.delta} for task {self.task_id}>'

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_total_points(cls):
        """計算目前所有積分的總和"""
        total = db.session.query(db.func.sum(cls.delta)).scalar()
        return total if total is not None else 0

    @classmethod
    def add_log(cls, task_id, delta, reason=None):
        """新增一筆積分變動紀錄"""
        new_log = cls(task_id=task_id, delta=delta, reason=reason)
        db.session.add(new_log)
        db.session.commit()
        return new_log
