from app import create_app

# 建立應用程式實例
app = create_app()

if __name__ == '__main__':
    # 啟動開發伺服器
    app.run(debug=True)
