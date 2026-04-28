# 流程圖文件（FLOWCHART）

**專案名稱**：TaskFlow — 個人任務管理系統
**文件版本**：v1.0
**建立日期**：2026-04-28
**參考文件**：`docs/PRD.md`、`docs/ARCHITECTURE.md`

---

## 1. 使用者流程圖（User Flow）

描述使用者在系統中的主要操作路徑。

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
    Validate -->|無效 - 標題空白| AddForm
    
    %% 標記完成 / 取消完成
    Action -->|點擊勾選框| Toggle[切換完成狀態]
    Toggle --> TaskStatus{任務原本狀態？}
    TaskStatus -->|未完成 → 已完成| AddPoints[累積積分\n新增 PointLog]
    TaskStatus -->|已完成 → 未完成| SubPoints[扣回積分\n新增 PointLog]
    AddPoints --> Home
    SubPoints --> Home
    
    %% 編輯任務
    Action -->|點擊編輯| EditPage[編輯頁面\n修改標題/積分]
    EditPage --> SaveEdit[按下「儲存」]
    SaveEdit --> Home
    
    %% 刪除任務
    Action -->|點擊刪除| Confirm{確認刪除？}
    Confirm -->|確認| DeleteTask[從資料庫移除]
    Confirm -->|取消| Home
    DeleteTask --> Home
    
    %% 查看積分歷程
    Action -->|查看積分歷程| LogPage[積分歷程頁面\n時間、任務名稱、分數]
    LogPage --> Home
```

---

## 2. 系統序列圖（Sequence Diagram）

描述「使用者操作」到「資料存入資料庫」的完整資料流。

### 2.1 新增任務流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route (tasks.py)
    participant Model as Task Model
    participant DB as SQLite

    User->>Browser: 填寫表單並點擊「新增」
    Browser->>Flask: POST /tasks/add (data: title, points)
    Flask->>Flask: 驗證資料 (標題不可為空)
    Flask->>Model: 建立 Task 物件 (is_done=False)
    Model->>DB: INSERT INTO tasks
    DB-->>Model: 成功
    Model-->>Flask: 回傳物件
    Flask-->>Browser: Redirect to / (302 Found)
    Browser->>Flask: GET /
    Flask->>DB: SELECT * FROM tasks
    DB-->>Flask: 任務列表
    Flask-->>Browser: Render index.html (200 OK)
```

### 2.2 切換完成狀態與積分變動

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route (tasks.py)
    participant TModel as Task Model
    participant PModel as PointLog Model
    participant DB as SQLite

    User->>Browser: 點擊任務勾選框
    Browser->>Flask: POST /tasks/<id>/toggle
    Flask->>TModel: 查詢 Task (id)
    TModel->>DB: SELECT * FROM tasks WHERE id=?
    DB-->>TModel: 任務資料
    
    alt 標記為完成 (is_done: False -> True)
        Flask->>TModel: 更新 is_done = True
        Flask->>PModel: 建立 PointLog (delta = +points)
    else 取消標記 (is_done: True -> False)
        Flask->>TModel: 更新 is_done = False
        Flask->>PModel: 建立 PointLog (delta = -points)
    end
    
    TModel->>DB: UPDATE tasks
    PModel->>DB: INSERT INTO point_logs
    DB-->>Flask: 成功
    Flask-->>Browser: Redirect to /
```

---

## 3. 功能清單對照表

根據架構設計與需求，定義各功能對應的技術細節。

| 功能名稱 | URL 路徑 | HTTP 方法 | 對應模板 (View) | 說明 |
|----------|----------|-----------|-----------------|------|
| 首頁 / 任務列表 | `/` | GET | `index.html` | 顯示所有任務與總積分 |
| 新增任務 | `/tasks/add` | POST | N/A (Redirect) | 處理表單提交，建立新任務 |
| 編輯任務頁面 | `/tasks/<id>/edit` | GET | `edit.html` | 顯示編輯表單 |
| 儲存編輯 | `/tasks/<id>/edit` | POST | N/A (Redirect) | 更新任務內容 |
| 刪除任務 | `/tasks/<id>/delete` | POST | N/A (Redirect) | 刪除任務 (積分歷程保留) |
| 切換完成狀態 | `/tasks/<id>/toggle` | POST | N/A (Redirect) | 切換狀態並記錄積分變動 |
| 積分歷程 | `/points/log` | GET | `point_log.html` | 顯示所有積分變動明細 |

---

*文件由 AI Agent (Flowchart Skill) 自動產出，請審閱流程邏輯是否符合預期。*
