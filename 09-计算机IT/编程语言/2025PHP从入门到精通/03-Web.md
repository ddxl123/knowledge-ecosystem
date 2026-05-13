# Web开发

## 核心知识点

### 一、表单处理

#### 1. 接收表单数据
```php
// GET请求
$name = $_GET['name'] ?? '';

// POST请求
$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';

// 过滤输入
$email = filter_input(INPUT_POST, 'email', FILTER_VALIDATE_EMAIL);
$age = filter_input(INPUT_POST, 'age', FILTER_VALIDATE_INT, [
    'options' => ['min_range' => 0, 'max_range' => 150]
]);
```

#### 2. 文件上传
```php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['avatar'])) {
    $file = $_FILES['avatar'];

    if ($file['error'] === UPLOAD_ERR_OK) {
        $allowed = ['image/jpeg', 'image/png', 'image/gif'];
        if (in_array($file['type'], $allowed)) {
            $filename = uniqid() . '_' . basename($file['name']);
            move_uploaded_file($file['tmp_name'], "uploads/$filename");
        }
    }
}
```

### 二、会话管理

#### 1. Session
```php
session_start();

// 设置
$_SESSION['user_id'] = 123;
$_SESSION['username'] = "Alice";

// 读取
$userId = $_SESSION['user_id'] ?? null;

// 销毁
session_destroy();
unset($_SESSION['user_id']);
```

#### 2. Cookie
```php
// 设置Cookie（有效期1小时）
setcookie("theme", "dark", time() + 3600, "/");

// 读取
$theme = $_COOKIE['theme'] ?? 'light';

// 删除
setcookie("theme", "", time() - 3600, "/");
```

### 三、HTTP请求与响应

```php
// 设置响应头
header('Content-Type: application/json');
http_response_code(200);

// JSON响应
echo json_encode(['status' => 'ok', 'data' => $data]);

// 重定向
header('Location: /login');
exit;

// 获取请求方法
$method = $_SERVER['REQUEST_METHOD'];

// 获取请求头
$auth = $_SERVER['HTTP_AUTHORIZATION'] ?? '';
```

### 四、cURL

```php
// GET请求
$ch = curl_init('https://api.example.com/data');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
curl_close($ch);
$data = json_decode($response, true);

// POST请求
$ch = curl_init('https://api.example.com/users');
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['name' => 'Alice']));
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
```

### 五、安全最佳实践

```php
// 防止SQL注入 - 使用预处理语句
$stmt = $pdo->prepare("SELECT * FROM users WHERE email = ?");
$stmt->execute([$email]);

// 防止XSS
$safe = htmlspecialchars($userInput, ENT_QUOTES, 'UTF-8');

// CSRF防护
session_start();
$token = bin2hex(random_bytes(32));
$_SESSION['csrf_token'] = $token;

// 表单中
echo '<input type="hidden" name="csrf_token" value="' . $token . '">';

// 验证
if (!hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'])) {
    die('CSRF token mismatch');
}

// 密码哈希
$hash = password_hash($password, PASSWORD_DEFAULT);
if (password_verify($inputPassword, $hash)) {
    // 密码正确
}
```

### 六、RESTful API

```php
// 路由处理
$method = $_SERVER['REQUEST_METHOD'];
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

switch ($method) {
    case 'GET':
        if (preg_match('/\/users\/(\d+)/', $path, $matches)) {
            // 获取单个用户
            getUser($matches[1]);
        } else {
            // 获取用户列表
            listUsers();
        }
        break;
    case 'POST':
        createUser();
        break;
    case 'PUT':
        updateUser();
        break;
    case 'DELETE':
        deleteUser();
        break;
}
```
