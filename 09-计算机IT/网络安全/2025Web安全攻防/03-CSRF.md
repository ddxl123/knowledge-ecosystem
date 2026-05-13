# CSRF攻防

## 核心知识点

### 一、攻击原理

```html
<!-- 攻击者页面 -->
<img src="https://bank.com/transfer?to=attacker&amount=10000" />

<!-- 或使用自动提交表单 -->
<form action="https://bank.com/transfer" method="POST" id="csrf-form">
    <input type="hidden" name="to" value="attacker" />
    <input type="hidden" name="amount" value="10000" />
</form>
<script>document.getElementById('csrf-form').submit();</script>
```

### 二、防御方案

#### 1. CSRF Token
```python
# Django自动CSRF防护
# 模板中
<form method="post">
    {% csrf_token %}
    <!-- 表单内容 -->
</form>

# 中间件已自动启用
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
]
```

```javascript
// 前端发送Token
fetch('/api/transfer', {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ to: 'user', amount: 100 })
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
```

#### 2. SameSite Cookie
```http
Set-Cookie: session=abc123; SameSite=Strict; Secure; HttpOnly
Set-Cookie: session=abc123; SameSite=Lax; Secure; HttpOnly
```

- **Strict：** 完全禁止第三方携带Cookie
- **Lax：** 允许GET请求携带Cookie（推荐）
- **None：** 允许所有请求携带（需配合Secure）

#### 3. 验证Referer/Origin
```python
def check_origin(request):
    origin = request.META.get('HTTP_ORIGIN', '')
    referer = request.META.get('HTTP_REFERER', '')
    allowed = ['https://example.com']

    if origin not in allowed and not referer.startswith('https://example.com'):
        return HttpResponseForbidden('Invalid origin')
```

#### 4. 双重Cookie验证
```javascript
// 前端
const csrfToken = getCookie('csrf_token');
fetch('/api/transfer', {
    method: 'POST',
    headers: {
        'X-CSRF-Token': csrfToken,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
});

// 后端验证：Cookie中的Token与Header中的Token一致
```

### 三、API安全

```javascript
// 使用Authorization头而非Cookie
fetch('/api/data', {
    headers: {
        'Authorization': 'Bearer ' + token
    }
});
// Authorization头不会被浏览器自动携带，天然防CSRF
```
