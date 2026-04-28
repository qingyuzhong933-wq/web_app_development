from flask_sqlalchemy import SQLAlchemy

# 初始化 SQLAlchemy 實例
db = SQLAlchemy()

def init_db(app):
    """初始化資料庫與應用程式的關聯"""
    db.init_app(app)
    with app.app_context():
        # 自動建立資料表 (如果不存在)
        db.create_all()
