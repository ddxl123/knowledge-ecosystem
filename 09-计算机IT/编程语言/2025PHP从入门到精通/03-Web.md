# Web开发

## HTTP请求与响应
- 超全局变量：`$_GET`获取URL参数、`$_POST`获取表单数据、`$_REQUEST`获取所有
- `$_SERVER`：请求方法（REQUEST_METHOD）、URL（REQUEST_URI）、IP（REMOTE_ADDR）
- 请求头：`getallheaders()` 或 `$_SERVER['HTTP_*']`
- 文件上传：`$_FILES`、`move_uploaded_file()` 移动临时文件
- 响应头：`header("Content-Type: application/json")`、`header("Location: /login")`
- HTTP方法判断：`$_SERVER['REQUEST_METHOD']` 或框架的Request对象

## Cookie与Session
- Cookie：存储在客户端，`setcookie("name", "value", time()+3600)`
- 读取Cookie：`$_COOKIE['name']`
- Session：存储在服务端，`session_start()` 启动
- Session操作：`$_SESSION['user'] = $data`、`unset($_SESSION['user'])`、`session_destroy()`
- Session存储：默认文件，可配置为Redis/Memcached/数据库
- Session安全：设置HttpOnly、Secure、SameSite属性，定期regenerate_id

## 表单处理
- 表单提交：`<form method="POST" action="/submit" enctype="multipart/form-data">`
- 数据验证：`filter_var($email, FILTER_VALIDATE_EMAIL)`、`filter_var($ip, FILTER_VALIDATE_IP)`
- 自定义验证：正则表达式、长度检查、范围检查
- CSRF防护：生成token存入session，表单中隐藏字段提交验证
- XSS防护：`htmlspecialchars($input, ENT_QUOTES, 'UTF-8')` 转义输出
- SQL注入防护：使用预处理语句（PDO/MySQLi），永远不要拼接SQL

## RESTful API
- 路由设计：`/api/users`（集合）、`/api/users/{id}`（单个资源）
- HTTP方法：GET获取、POST创建、PUT更新、DELETE删除
- JSON响应：`header("Content-Type: application/json"); echo json_encode($data);`
- 状态码：`http_response_code(201)` 设置HTTP状态码
- 认证方式：Session认证、JWT Token、API Key、OAuth 2.0
- CORS跨域：`header("Access-Control-Allow-Origin: *")` 及相关头
- API版本控制：URL路径（/api/v1/users）或请求头

## 常用Web功能
- 文件操作：`file_get_contents()`读取、`file_put_contents()`写入、`fopen/fread/fwrite`
- 图片处理：GD库（`imagecreate()`、`imagejpeg()`）、Imagick扩展
- 邮件发送：`mail()`函数、PHPMailer库、SwiftMailer/Symfony Mailer
- 缓存：`file_put_contents()`文件缓存、APCu内存缓存、Redis/Memcached
- 日志：`error_log()`、Monolog日志库
- 定时任务：Cron + PHP CLI脚本 `php /path/to/script.php`
- 国际化：`gettext()`、intl扩展（IntlDateFormatter、NumberFormatter）
