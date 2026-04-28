# 路由設計文件（ROUTES）

**專案名稱**：TaskFlow — 個人任務管理系統
**文件版本**：v1.0
**建立日期**：2026-04-28
**參考文件**：`docs/PRD.md`、`docs/ARCHITECTURE.md`、`docs/DB_DESIGN.md`

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| **任務列表 (首頁)** | GET | `/` | `index.html` | 顯示所有任務與總積分 |
| **新增任務** | POST | `/tasks/add` | — | 接收表單，建立新任務後重導向 |
| **編輯任務頁面** | GET | `/tasks/<int:id>/edit` | `edit.html` | 顯示帶有現有資料的編輯表單 |
| **儲存編輯內容** | POST | `/tasks/<int:id>/edit` | — | 更新任務標題、描述、積分與日期 |
| **切換完成狀態** | POST | `/tasks/<int:id>/toggle` | — | 切換 is_done 並同步記錄 PointLog |
| **刪除任務** | POST | `/tasks/<int:id>/delete` | — | 刪除指定任務 (PointLog 保留) |
| **積分歷程頁面** | GET | `/points/log` | `point_log.html` | 顯示所有積分變動明細與總分 |

---

## 2. 每個路由的詳細說明

### 2.1 任務列表 (首頁)
- **URL**: `/` (GET)
- **邏輯**:
    1. 呼叫 `Task.get_all()` 取得任務清單。
    2. 呼叫 `PointLog.get_total_points()` 取得目前總分。
- **輸出**: 渲染 `index.html`，傳入 `tasks` 與 `total_points`。

### 2.2 新增任務
- **URL**: `/tasks/add` (POST)
- **輸入**: 表單欄位 `title`, `points` (選填), `description` (選填), `due_date` (選填)。
- **邏輯**: 呼叫 `Task.create()` 存入資料庫。
- **輸出**: 重導向至 `/`。

### 2.3 編輯任務頁面
- **URL**: `/tasks/<id>/edit` (GET)
- **處理**: 呼叫 `Task.get_by_id(id)`，若不存在則回傳 404。
- **輸出**: 渲染 `edit.html`，傳入 `task` 物件。

### 2.4 切換完成狀態
- **URL**: `/tasks/<id>/toggle` (POST)
- **邏輯**: 
    1. 取得任務資訊。
    2. 切換 `is_done` 狀態。
    3. 若變為「完成」：新增一筆 `PointLog(delta=+task.points)`。
    4. 若變為「未完成」：新增一筆 `PointLog(delta=-task.points)`。
- **輸出**: 重導向至 `/`。

### 2.5 刪除任務
- **URL**: `/tasks/<id>/delete` (POST)
- **邏輯**: 呼叫 `task.delete()`。
- **輸出**: 重導向至 `/`。

---

## 3. Jinja2 模板清單

所有模板皆存儲於 `app/templates/`。

| 檔案名稱 | 繼承自 | 說明 |
|----------|--------|------|
| `base.html` | — | 基礎佈局（包含導覽列、總分顯示、CSS/JS 引入） |
| `index.html` | `base.html` | 任務清單首頁、快速新增表單 |
| `edit.html` | `base.html` | 編輯任務詳情頁面 |
| `point_log.html` | `base.html` | 積分歷史變動明細頁面 |

---

## 4. 路由骨架規劃

我們將使用 Flask Blueprint 來拆分功能：
- `app/routes/tasks.py`：處理所有與任務相關的操作。
- `app/routes/points.py`：處理與積分顯示相關的操作。

---

*文件由 AI Agent (API Design Skill) 自動產出，請根據實際需求調整。*
