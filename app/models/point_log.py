from datetime import datetime
from app.models import db

class PointLog(db.Model):
    """
    積分歷程模型 (PointLog Model)
    記錄每一次積分的增減紀錄。
    """
    __tablename__ = 'point_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, nullable=True)  # 關聯任務 ID
    delta = db.Column(db.Integer, nullable=False)   # 積分變動值 (+/-)
    reason = db.Column(db.String(200), nullable=True) # 變動原因
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<PointLog {self.delta} for task {self.task_id}>'

    @classmethod
    def get_all(cls):
        """取得所有積分變動紀錄，依時間倒序排列"""
        try:
            return cls.query.order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error getting point logs: {e}")
            return []

    @classmethod
    def get_total_points(cls):
        """計算目前所有積分的總和"""
        try:
            total = db.session.query(db.func.sum(cls.delta)).scalar()
            return total if total is not None else 0
        except Exception as e:
            print(f"Error calculating total points: {e}")
            return 0

    @classmethod
    def add_log(cls, task_id, delta, reason=None):
        """
        新增一筆積分變動紀錄
        :param task_id: 任務 ID
        :param delta: 變動值 (+/-)
        :param reason: 原因 (通常是任務標題)
        """
        try:
            new_log = cls(task_id=task_id, delta=delta, reason=reason)
            db.session.add(new_log)
            db.session.commit()
            return new_log
        except Exception as e:
            db.session.rollback()
            print(f"Error adding point log: {e}")
            return None
