# CSRF 跨站请求伪造


## 收集指南

> ⚠️ **严格范围限定：** 仅收集本章（第3章 CSRF）相关内容，禁止跨章节引用。

### 条目描述
本文件是《2025Web安全攻防》中关于「CSRF」的知识原子文件，属于网络安全方向。

### 知识结构
- CSRF 原理
- 攻击场景
- 检测方法
- 防御措施
- SameSite Cookie

### 待收集原子知识点
- CSRF 攻击原理
- GET/POST CSRF
- CSRF Token 机制
- SameSite Cookie 属性
- Referer/Origin 校验

## 核心知识点

### 一、CSRF 原理

- **攻击原理：** 利用用户已登录的身份，诱导用户访问恶意页面，自动发送伪造请求
- **前提条件：**
  - 用户已登录目标网站（Cookie 中有会话信息）
  - 目标网站仅依赖 Cookie 验证身份
  - 攻击者知道请求的格式和目标 URL

```html
<!-- 恶意页面中的自动提交表单 -->
<form action="http://bank.com/transfer" method="POST" id="csrf">
    <input name="to" value="attacker_account">
    <input name="amount" value="10000">
</form>
<script>document.getElementById('csrf').submit();</script>

<!-- GET 请求的 CSRF（更简单） -->
<img src="http://bank.com/transfer?to=attacker&amount=10000">
```

### 二、防御措施

```python
# 1. CSRF Token（最常用）
# Django 内置
# 模板中: {% csrf_token %}
# 中间件: CsrfViewMiddleware（默认启用）

# Flask + Flask-WTF
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# 2. SameSite Cookie 属性
Set-Cookie: session=abc123; SameSite=Strict  # 完全禁止跨站携带
Set-Cookie: session=abc123; SameSite=Lax     # GET 允许，POST 禁止（推荐）

# 3. 验证 Referer/Origin 头
def check_origin(request):
    origin = request.headers.get('Origin')
    if origin and origin not in ALLOWED_ORIGINS:
        return False
    return True

# 4. 自定义请求头（AJAX 请求）
# 浏览器不会在跨站请求中携带自定义头
headers: { 'X-Requested-With': 'XMLHttpRequest' }
```

### 三、SameSite Cookie 详解

- **Strict：** 完全禁止跨站发送 Cookie（最安全但影响用户体验）
- **Lax：** 顶级导航的 GET 请求允许，POST 禁止（Chrome 默认）
- **None：** 允许跨站发送（必须同时设置 Secure）

### 四、Token vs SameSite 对比

- **CSRF Token：** 需要服务端生成和验证，前后端配合
- **SameSite Cookie：** 浏览器层面防护，零代码修改
- **建议：** 两者结合使用，形成双重防护

### 五、最佳实践

- 所有状态修改请求（POST/PUT/DELETE）必须验证 CSRF Token
- Cookie 设置 `SameSite=Lax` 或 `Strict`
- 关键操作增加二次验证（如密码确认）
- 使用 `HttpOnly` + `Secure` Cookie
- 避免在 URL 中传递敏感信息（GET 请求）
