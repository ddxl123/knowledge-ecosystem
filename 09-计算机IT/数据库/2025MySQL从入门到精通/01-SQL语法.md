# MySQL SQL 语法


## 收集指南

> ⚠️ **严格范围限定：** 仅收集本章（第1章 SQL语法）相关内容，禁止跨章节引用。

### 条目描述
本文件是《2025MySQL从入门到精通》中关于「SQL语法」的知识原子文件，属于数据库方向。

### 知识结构
- SQL 基础语法
- 数据定义（DDL）
- 数据操作（DML）
- 数据查询（DQL）
- 函数与表达式

### 待收集原子知识点
- SQL 语言分类与基础
- CREATE/ALTER/DROP 语句
- INSERT/UPDATE/DELETE 语句
- SELECT 查询与子查询
- 内置函数与窗口函数

## 核心知识点

### 一、SQL 语言分类

- **DDL（数据定义语言）：** CREATE、ALTER、DROP、TRUNCATE
- **DML（数据操作语言）：** INSERT、UPDATE、DELETE
- **DQL（数据查询语言）：** SELECT
- **DCL（数据控制语言）：** GRANT、REVOKE
- **TCL（事务控制语言）：** COMMIT、ROLLBACK、SAVEPOINT

### 二、数据定义（DDL）

```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS mydb
    DEFAULT CHARSET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- 创建表
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    password CHAR(60) NOT NULL,
    age TINYINT UNSIGNED DEFAULT 0,
    status ENUM('active', 'inactive', 'banned') DEFAULT 'active',
    profile JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_status_created (status, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 修改表结构
ALTER TABLE users ADD COLUMN phone VARCHAR(20) AFTER email;
ALTER TABLE users MODIFY COLUMN username VARCHAR(100) NOT NULL;
ALTER TABLE users DROP COLUMN phone;
ALTER TABLE users ADD INDEX idx_username (username);

-- 删除表
DROP TABLE IF EXISTS users;
TRUNCATE TABLE users;  -- 清空表数据，重置自增ID
```

### 三、数据操作（DML）

```sql
-- 插入
INSERT INTO users (username, email, password) VALUES ('alice', 'alice@mail.com', 'hashed_pw');
INSERT INTO users (username, email, password) VALUES
    ('bob', 'bob@mail.com', 'hashed_pw'),
    ('charlie', 'charlie@mail.com', 'hashed_pw');

-- 插入或更新（冲突时更新）
INSERT INTO users (username, email) VALUES ('alice', 'new@mail.com')
ON DUPLICATE KEY UPDATE email = VALUES(email);

-- 更新
UPDATE users SET status = 'inactive' WHERE created_at < '2024-01-01';
UPDATE users SET age = age + 1 WHERE status = 'active' LIMIT 100;

-- 删除
DELETE FROM users WHERE status = 'banned' AND created_at < '2023-01-01';
DELETE FROM users ORDER BY created_at ASC LIMIT 100;  -- 删除最早的100条
```

### 四、数据查询（DQL）

```sql
-- 基础查询
SELECT id, username, email FROM users WHERE status = 'active' ORDER BY created_at DESC;

-- 条件查询
SELECT * FROM users WHERE age BETWEEN 18 AND 30;
SELECT * FROM users WHERE username IN ('alice', 'bob');
SELECT * FROM users WHERE email LIKE '%@gmail.com';
SELECT * FROM users WHERE profile->'$.city' = 'Beijing';  -- JSON 查询

-- 聚合查询
SELECT status, COUNT(*) as count, AVG(age) as avg_age
FROM users GROUP BY status HAVING count > 10;

-- 连接查询
SELECT u.username, o.order_no, o.amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.status = 'paid';

SELECT u.username, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;

-- 子查询
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE amount > 1000);
SELECT * FROM users WHERE age > (SELECT AVG(age) FROM users);

-- EXISTS 子查询
SELECT * FROM users u WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.status = 'paid'
);

-- 分页
SELECT * FROM users ORDER BY id LIMIT 20 OFFSET 0;  -- 第1页
SELECT * FROM users WHERE id > 100 ORDER BY id LIMIT 20;  -- 游标分页（推荐）
```

### 五、窗口函数（MySQL 8.0+）

```sql
-- ROW_NUMBER
SELECT username, score,
    ROW_NUMBER() OVER (ORDER BY score DESC) as ranking
FROM users;

-- 分组排名
SELECT username, department, score,
    RANK() OVER (PARTITION BY department ORDER BY score DESC) as dept_rank
FROM users;

-- 累计求和
SELECT order_date, amount,
    SUM(amount) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) as cumulative
FROM orders;

-- LAG/LEAD（前后行值）
SELECT month, revenue,
    LAG(revenue, 1) OVER (ORDER BY month) as prev_month,
    revenue - LAG(revenue, 1) OVER (ORDER BY month) as growth
FROM monthly_stats;

-- NTILE（分桶）
SELECT username, score,
    NTILE(4) OVER (ORDER BY score DESC) as quartile
FROM users;
```
