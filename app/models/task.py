from datetime import datetime
from app.models import db

class Task(db.Model):
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
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, task_id):
        return cls.query.get(task_id)

    @classmethod
    def create(cls, title, points=10, description=None, due_date=None):
        new_task = cls(
            title=title,
            points=points,
            description=description,
            due_date=due_date
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task

    def update(self, title=None, points=None, description=None, due_date=None, is_done=None):
        if title is not None: self.title = title
        if points is not None: self.points = points
        if description is not None: self.description = description
        if due_date is not None: self.due_date = due_date
        if is_done is not None: self.is_done = is_done
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
