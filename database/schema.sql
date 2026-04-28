-- TaskFlow Database Schema
-- Last Updated: 2026-04-28

-- 建立任務表
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    points INTEGER DEFAULT 10,
    is_done BOOLEAN DEFAULT 0,
    due_date DATETIME,
    created_at DATETIME DEFAULT (datetime('now', 'localtime'))
);

-- 建立積分歷程表
CREATE TABLE IF NOT EXISTS point_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    delta INTEGER NOT NULL,
    reason TEXT,
    created_at DATETIME DEFAULT (datetime('now', 'localtime'))
);

-- 建立索引以提升查詢效能
CREATE INDEX IF NOT EXISTS idx_tasks_is_done ON tasks(is_done);
CREATE INDEX IF NOT EXISTS idx_point_logs_created_at ON point_logs(created_at);
