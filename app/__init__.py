import os
from flask import Flask
from app.models import db, init_db

def create_app():
    """建立並設定 Flask 應用程式"""
    app = Flask(__name__, instance_relative_config=True)
    
    # 預設設定
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'database.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化資料庫
    init_db(app)

    # 註冊藍圖 (Blueprints)
    from app.routes.tasks import tasks_bp
    from app.routes.points import points_bp
    
    app.register_blueprint(tasks_bp)
    app.register_blueprint(points_bp)

    return app
