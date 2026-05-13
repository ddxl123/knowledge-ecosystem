# SQL语法基础

## 核心知识点

### 一、DDL（数据定义语言）

#### 1. 数据库操作
```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS mydb
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE mydb;

-- 删除数据库
DROP DATABASE IF EXISTS mydb;
```

#### 2. 表操作
```sql
-- 创建表
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    age INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username_email (username, email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 修改表
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
ALTER TABLE users MODIFY COLUMN phone VARCHAR(30);
ALTER TABLE users DROP COLUMN phone;
ALTER TABLE users RENAME TO members;

-- 删除表
DROP TABLE IF EXISTS users;
```

### 二、DML（数据操作语言）

#### 1. 插入数据
```sql
-- 单条插入
INSERT INTO users (username, email, age) VALUES ('alice', 'alice@example.com', 25);

-- 批量插入
INSERT INTO users (username, email, age) VALUES
    ('bob', 'bob@example.com', 30),
    ('charlie', 'charlie@example.com', 28);

-- 插入或更新
INSERT INTO users (username, email) VALUES ('alice', 'new@example.com')
ON DUPLICATE KEY UPDATE email = VALUES(email);
```

#### 2. 更新数据
```sql
UPDATE users SET age = 26 WHERE username = 'alice';
UPDATE users SET age = age + 1 WHERE age < 30;
```

#### 3. 删除数据
```sql
DELETE FROM users WHERE id = 1;
DELETE FROM users WHERE age < 18;
TRUNCATE TABLE users;  -- 清空表，重置自增ID
```

### 三、DQL（数据查询语言）

#### 1. 基础查询
```sql
-- 查询所有列
SELECT * FROM users;

-- 查询指定列
SELECT username, email FROM users;

-- 条件查询
SELECT * FROM users WHERE age >= 18 AND age <= 30;
SELECT * FROM users WHERE age BETWEEN 18 AND 30;
SELECT * FROM users WHERE username IN ('alice', 'bob');
SELECT * FROM users WHERE email LIKE '%@gmail.com';
SELECT * FROM users WHERE phone IS NULL;
```

#### 2. 排序与分页
```sql
-- 排序
SELECT * FROM users ORDER BY age DESC, username ASC;

-- 分页
SELECT * FROM users LIMIT 10 OFFSET 0;  -- 第1页
SELECT * FROM users LIMIT 10 OFFSET 10; -- 第2页
```

#### 3. 聚合函数
```sql
SELECT 
    COUNT(*) AS total,
    AVG(age) AS avg_age,
    MAX(age) AS max_age,
    MIN(age) AS min_age,
    SUM(age) AS sum_age
FROM users;

-- 分组
SELECT age, COUNT(*) AS count
FROM users
GROUP BY age
HAVING count > 5;
```

#### 4. 连接查询
```sql
-- 内连接
SELECT u.username, o.order_no
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- 左连接
SELECT u.username, o.order_no
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- 右连接
SELECT u.username, o.order_no
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;
```

#### 5. 子查询
```sql
-- WHERE子查询
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);

-- FROM子查询
SELECT * FROM (
    SELECT user_id, COUNT(*) AS order_count
    FROM orders GROUP BY user_id
) AS t WHERE t.order_count > 5;

-- EXISTS子查询
SELECT * FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);
```

### 四、DCL（数据控制语言）
```sql
-- 创建用户
CREATE USER 'app_user'@'%' IDENTIFIED BY 'password';

-- 授权
GRANT SELECT, INSERT, UPDATE ON mydb.* TO 'app_user'@'%';

-- 撤销权限
REVOKE INSERT ON mydb.* FROM 'app_user'@'%';

-- 查看权限
SHOW GRANTS FOR 'app_user'@'%';
```

### 五、窗口函数（MySQL 8.0+）
```sql
-- ROW_NUMBER
SELECT username, age,
    ROW_NUMBER() OVER (ORDER BY age DESC) AS rn
FROM users;

-- RANK
SELECT username, score,
    RANK() OVER (ORDER BY score DESC) AS rank_num
FROM students;

-- 分组排名
SELECT username, department, salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;

-- 累计求和
SELECT order_date, amount,
    SUM(amount) OVER (ORDER BY order_date) AS running_total
FROM orders;
```
