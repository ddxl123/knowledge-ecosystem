# Node.js Express


## 收集指南

> ⚠️ **严格范围限定：** 仅收集本章（第1章 Express）相关内容，禁止跨章节引用。

### 条目描述
本文件是《2025Node.js实战》中关于「Express」的知识原子文件，属于后端开发方向。

### 知识结构
- Express 基础与路由
- 中间件机制
- 请求与响应处理
- 错误处理
- 模板引擎

### 待收集原子知识点
- Express 应用创建与路由
- 中间件类型与执行流程
- 请求参数与响应方法
- 错误处理中间件
- 模板引擎集成

## 核心知识点

### 一、Express 基础与路由

```javascript
const express = require('express');
const app = express();

// 基础中间件
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 路由定义
app.get('/api/users', (req, res) => {
    const { page = 1, size = 20, keyword } = req.query;
    // 查询逻辑...
    res.json({ data: users, total, page: +page, size: +size });
});

app.get('/api/users/:id', (req, res) => {
    const user = users.find(u => u.id === +req.params.id);
    if (!user) return res.status(404).json({ error: '用户不存在' });
    res.json(user);
});

app.post('/api/users', (req, res) => {
    const { username, email } = req.body;
    const user = { id: Date.now(), username, email };
    users.push(user);
    res.status(201).json(user);
});

app.put('/api/users/:id', (req, res) => { /* 更新逻辑 */ });
app.delete('/api/users/:id', (req, res) => { /* 删除逻辑 */ });

// 路由模块化
const userRouter = require('./routes/users');
app.use('/api/users', userRouter);

app.listen(3000, () => console.log('Server running on port 3000'));
```

```javascript
// routes/users.js
const router = require('express').Router();

router.get('/', async (req, res, next) => {
    try {
        const users = await User.findAll();
        res.json(users);
    } catch (err) {
        next(err);
    }
});

router.get('/:id', async (req, res, next) => {
    try {
        const user = await User.findById(req.params.id);
        if (!user) return res.status(404).json({ error: 'Not found' });
        res.json(user);
    } catch (err) {
        next(err);
    }
});

module.exports = router;
```

### 二、中间件机制

```javascript
// 应用级中间件
app.use((req, res, next) => {
    req.startTime = Date.now();
    console.log(`${req.method} ${req.url}`);
    next();
});

// 路由级中间件
const authMiddleware = (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).json({ error: '未认证' });
    try {
        req.user = jwt.verify(token, SECRET);
        next();
    } catch {
        res.status(401).json({ error: 'Token 无效' });
    }
};

router.get('/profile', authMiddleware, (req, res) => {
    res.json(req.user);
});

// 第三方中间件
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');

app.use(cors());
app.use(helmet());
app.use(morgan('combined'));
app.use(rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }));

// 静态文件
app.use(express.static('public'));
app.use('/uploads', express.static('uploads'));
```

### 三、请求与响应处理

```javascript
// 请求对象
app.post('/api/search', (req, res) => {
    req.params    // 路由参数 /:id
    req.query     // 查询参数 ?page=1
    req.body      // 请求体（JSON/表单）
    req.headers   // 请求头
    req.ip        // 客户端 IP
    req.files     // 文件上传（需 multer）
    req.get('Content-Type')  // 获取指定请求头
});

// 响应方法
res.json({ data });           // JSON 响应
res.status(201).json(data);   // 设置状态码 + JSON
res.send('Hello');            // 文本/HTML 响应
res.redirect('/login');       // 重定向
res.download('file.pdf');     // 文件下载
res.render('index', { title });// 模板渲染
res.set('X-Custom', 'value'); // 设置响应头
res.cookie('token', value, { httpOnly: true, maxAge: 3600000 });
res.clearCookie('token');
```

### 四、错误处理

```javascript
// 自定义错误类
class AppError extends Error {
    constructor(message, statusCode) {
        super(message);
        this.statusCode = statusCode;
        this.isOperational = true;
    }
}

// 异步包装器
const asyncHandler = (fn) => (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
};

// 使用
router.get('/:id', asyncHandler(async (req, res) => {
    const user = await User.findById(req.params.id);
    if (!user) throw new AppError('用户不存在', 404);
    res.json(user);
}));

// 全局错误处理中间件（必须4个参数）
app.use((err, req, res, next) => {
    const statusCode = err.statusCode || 500;
    const message = err.isOperational ? err.message : '服务器内部错误';
    
    console.error(`[ERROR] ${err.message}`, { stack: err.stack });
    
    res.status(statusCode).json({
        error: message,
        ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    });
});
```

### 五、文件上传（Multer）

```javascript
const multer = require('multer');
const path = require('path');

const storage = multer.diskStorage({
    destination: (req, file, cb) => cb(null, 'uploads/'),
    filename: (req, file, cb) => {
        const uniqueName = `${Date.now()}-${Math.round(Math.random() * 1E9)}`;
        cb(null, uniqueName + path.extname(file.originalname));
    }
});

const upload = multer({
    storage,
    limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
    fileFilter: (req, file, cb) => {
        const allowed = /jpeg|jpg|png|gif|pdf/;
        const ext = allowed.test(path.extname(file.originalname).toLowerCase());
        const mime = allowed.test(file.mimetype);
        cb(null, ext && mime);
    }
});

app.post('/api/upload', upload.single('file'), (req, res) => {
    res.json({ filename: req.file.filename, path: req.file.path });
});

app.post('/api/uploads', upload.array('files', 5), (req, res) => {
    res.json({ files: req.files.map(f => f.filename) });
});
```
