# 流程圖文件（FLOWCHART）

**專案名稱**：TaskFlow — 個人任務管理系統
**文件版本**：v1.0
**建立日期**：2026-04-15
**參考文件**：`docs/PRD.md`、`docs/ARCHITECTURE.md`

---

## 1. 使用者流程圖（User Flow）

描述使用者從進入網站到完成各項操作的完整路徑。

```mermaid
flowchart LR
    Start([🚀 使用者開啟網頁]) --> Home[首頁\n任務清單 + 總積分]

    Home --> Action{要執行什麼操作？}

    %% 新增任務
    Action -->|新增任務| AddForm[填寫任務標題\n設定積分值]
    AddForm --> Submit[按下「新增」]
    Submit --> Validate{輸入是否有效？}
    Validate -->|有效| SaveTask[儲存至資料庫]
    SaveTask --> Home
    Validate -->|無效 - 欄位空白| AddForm

    %% 標記完成
    Action -->|標記完成| Toggle[勾選任務 Checkbox]
    Toggle --> AlreadyDone{任務已完成？}
    AlreadyDone -->|否 → 標記完成| AddPoint[累積積分\n新增 PointLog]
    AlreadyDone -->|是 → 取消完成| SubPoint[扣回積分\n更新 PointLog]
    AddPoint --> Home
    SubPoint --> Home

    %% 編輯任務
    Action -->|編輯任務| EditForm[編輯頁面\n修改標題/積分]
    EditForm --> SaveEdit[按下「儲存」]
    SaveEdit --> Home

    %% 刪除任務
    Action -->|刪除任務| Confirm{確認刪除？}
    Confirm -->|取消| Home
    Confirm -->|確認| DeleteTask[從資料庫移除]
    DeleteTask --> Home

    %% 查看積分歷程
    Action -->|查看積分歷程| LogPage[積分歷程頁面\n時間、任務名稱、分數]
    LogPage --> Home
```

---

## 2. 系統序列圖（Sequence Diagram）

描述各主要功能在系統元件之間的資料流動順序。

### 2.1 新增任務

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Flask as 📋 Flask Route
    participant Model as 🗄️ Task Model
    participant DB as 💾 SQLite

    User->>Browser: 填寫任務標題與積分，按下「新增」
    Browser->>Flask: POST /tasks/add
    Flask->>Flask: 驗證表單資料（標題不可空白）
    Flask->>Model: Task(title, points, is_done=False)
    Model->>DB: INSERT INTO tasks
    DB-->>Model: 回傳新建任務 ID
    Model-->>Flask: 任務物件
    Flask-->>Browser: redirect → GET /（首頁）
    Browser-->>User: 顯示更新後的任務清單
```

---

### 2.2 標記任務完成（Toggle）

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Flask as 📋 Flask Route
    participant TaskModel as 🗄️ Task Model
    participant PointModel as 🏆 PointLog Model
    participant DB as 💾 SQLite

    User->>Browser: 點擊任務旁的勾選框
    Browser->>Flask: POST /tasks/<id>/toggle

    Flask->>TaskModel: 查詢 Task by ID
    TaskModel->>DB: SELECT * FROM tasks WHERE id=?
    DB-->>TaskModel: 任務資料
    TaskModel-->>Flask: Task 物件

    alt 任務未完成 → 標記完成
        Flask->>TaskModel: task.is_done = True
        Flask->>PointModel: 新增 PointLog(task_id, +points)
    else 任務已完成 → 取消完成
        Flask->>TaskModel: task.is_done = False
        Flask->>PointModel: 新增 PointLog(task_id, -points)
    end

    TaskModel->>DB: UPDATE tasks SET is_done=?
    PointModel->>DB: INSERT INTO point_logs
    DB-->>Flask: 更新成功
    Flask-->>Browser: redirect → GET /
    Browser-->>User: 顯示更新後積分與任務狀態
```

---

### 2.3 編輯任務

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Flask as 📋 Flask Route
    participant Model as 🗄️ Task Model
    participant DB as 💾 SQLite

    User->>Browser: 點擊「編輯」按鈕
    Browser->>Flask: GET /tasks/<id>/edit
    Flask->>Model: 查詢 Task by ID
    Model->>DB: SELECT * FROM tasks WHERE id=?
    DB-->>Model: 任務資料
    Model-->>Flask: Task 物件
    Flask-->>Browser: render edit.html（帶入現有資料）
    Browser-->>User: 顯示編輯表單

    User->>Browser: 修改內容後按下「儲存」
    Browser->>Flask: POST /tasks/<id>/edit
    Flask->>Model: task.title = new_title, task.points = new_points
    Model->>DB: UPDATE tasks SET title=?, points=? WHERE id=?
    DB-->>Flask: 更新成功
    Flask-->>Browser: redirect → GET /
    Browser-->>User: 顯示更新後的清單
```

---

### 2.4 刪除任務

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Flask as 📋 Flask Route
    participant Model as 🗄️ Task Model
    participant DB as 💾 SQLite

    User->>Browser: 點擊「刪除」按鈕
    Browser-->>User: 彈出確認對話框（JS confirm）

    alt 使用者按下「確認」
        Browser->>Flask: POST /tasks/<id>/delete
        Flask->>Model: 查詢 Task by ID
        Model->>DB: SELECT * FROM tasks WHERE id=?
        DB-->>Model: 任務資料
        Flask->>Model: db.session.delete(task)
        Model->>DB: DELETE FROM tasks WHERE id=?
        DB-->>Flask: 刪除成功（PointLog 保留不刪）
        Flask-->>Browser: redirect → GET /
        Browser-->>User: 顯示更新後的清單
    else 使用者按下「取消」
        Browser-->>User: 關閉對話框，不做任何操作
    end
```

---

### 2.5 查看積分歷程

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Flask as 📋 Flask Route
    participant Model as 🏆 PointLog Model
    participant DB as 💾 SQLite

    User->>Browser: 點擊「積分歷程」連結
    Browser->>Flask: GET /points/log
    Flask->>Model: PointLog.query.order_by(created_at DESC)
    Model->>DB: SELECT * FROM point_logs ORDER BY created_at DESC
    DB-->>Model: 所有積分紀錄
    Model-->>Flask: PointLog 列表
    Flask->>DB: SELECT SUM(delta) FROM point_logs（計算總積分）
    DB-->>Flask: 總積分數值
    Flask-->>Browser: render point_log.html
    Browser-->>User: 顯示積分歷程列表與總積分
```

---

## 3. 功能清單對照表

| 功能 | URL 路徑 | HTTP Method | 說明 |
|------|----------|-------------|------|
| 首頁（任務清單） | `/` | GET | 顯示所有任務與目前總積分 |
| 新增任務 | `/tasks/add` | POST | 接收表單，建立新任務 |
| 編輯任務（表單） | `/tasks/<id>/edit` | GET | 顯示帶有現有資料的編輯表單 |
| 儲存編輯 | `/tasks/<id>/edit` | POST | 更新任務標題與積分 |
| 刪除任務 | `/tasks/<id>/delete` | POST | 刪除指定任務（積分歷程保留） |
| 切換完成狀態 | `/tasks/<id>/toggle` | POST | 切換 is_done，並更新積分紀錄 |
| 積分歷程 | `/points/log` | GET | 顯示所有積分變動紀錄 |

---

*文件由 AI Agent（Flowchart Skill）自動產出，請團隊審閱後修改調整。*
