# BOM操作

## 核心知识点

### 一、window对象

#### 1. 全局作用域
```javascript
// 全局变量和函数都是window的属性
var name = "Alice";
console.log(window.name); // "Alice"

// 全局方法
window.alert("Hello");
window.confirm("Are you sure?");
window.prompt("Enter your name:");
```

#### 2. 定时器
```javascript
// 延时执行
const timerId = setTimeout(() => {
    console.log("1秒后执行");
}, 1000);
clearTimeout(timerId);

// 间隔执行
const intervalId = setInterval(() => {
    console.log("每2秒执行");
}, 2000);
clearInterval(intervalId);

// requestAnimationFrame
function animate() {
    // 动画逻辑
    requestAnimationFrame(animate);
}
animate();
```

### 二、location对象

#### 1. URL信息
```javascript
location.href;      // 完整URL
location.protocol;  // 协议（http:）
location.host;      // 主机名和端口
location.hostname;  // 主机名
location.port;      // 端口
location.pathname;  // 路径
location.search;    // 查询字符串
location.hash;      // 锚点
```

#### 2. 页面跳转
```javascript
location.assign("https://example.com");
location.replace("https://example.com"); // 不保留历史
location.reload(); // 刷新页面
```

### 三、history对象
```javascript
history.back();     // 后退
history.forward();  // 前进
history.go(-2);     // 后退2步
history.pushState({page: 1}, "Title", "/page1");
history.replaceState({page: 1}, "Title", "/page1");
```

### 四、navigator对象
```javascript
navigator.userAgent;    // 浏览器信息
navigator.language;     // 语言
navigator.platform;     // 平台
navigator.onLine;       // 是否在线
navigator.geolocation;  // 地理位置
navigator.clipboard;    // 剪贴板
```

### 五、localStorage/sessionStorage
```javascript
// localStorage（持久存储）
localStorage.setItem("key", "value");
localStorage.getItem("key");
localStorage.removeItem("key");
localStorage.clear();

// sessionStorage（会话存储，关闭标签页清除）
sessionStorage.setItem("key", "value");
sessionStorage.getItem("key");

// 存储对象
localStorage.setItem("user", JSON.stringify({name: "Alice", age: 25}));
const user = JSON.parse(localStorage.getItem("user"));
```
