# Express框架

## 核心知识点

### 一、基本服务器

```javascript
const express = require('express');
const app = express();
const PORT = 3000;

// 中间件
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 路由
app.get('/', (req, res) => {
    res.json({ message: 'Hello, Express!' });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
```

### 二、路由

```javascript
// 基本路由
app.get('/users', (req, res) => {
    res.json(users);
});

app.post('/users', (req, res) => {
    const user = req.body;
    users.push(user);
    res.status(201).json(user);
});

app.put('/users/:id', (req, res) => {
    const { id } = req.params;
    const updatedUser = req.body;
    // 更新逻辑...
    res.json(updatedUser);
});

app.delete('/users/:id', (req, res) => {
    const { id } = req.params;
    // 删除逻辑...
    res.status(204).send();
});

// 路由组
const router = express.Router();

router.get('/', userController.list);
router.get('/:id', userController.get);
router.post('/', userController.create);
router.put('/:id', userController.update);
router.delete('/:id', userController.delete);

app.use('/api/users', router);
```

### 三、中间件

```javascript
// 日志中间件
const logger = (req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
    next();
};
app.use(logger);

// 错误处理中间件
const errorHandler = (err, req, res, next) => {
    console.error(err.stack);
    res.status(err.status || 500).json({
        error: err.message || 'Internal Server Error'
    });
};
app.use(errorHandler);

// 认证中间件
const authenticate = (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) {
        return res.status(401).json({ error: 'No token provided' });
    }
    try {
        const decoded = jwt.verify(token, SECRET_KEY);
        req.user = decoded;
        next();
    } catch (err) {
        res.status(401).json({ error: 'Invalid token' });
    }
};

// 使用中间件
app.get('/protected', authenticate, (req, res) => {
    res.json({ user: req.user });
});
```

### 四、请求与响应

```javascript
// 请求参数
app.get('/search', (req, res) => {
    const { q, page = 1, limit = 10 } = req.query;
    res.json({ query: q, page, limit });
});

// 请求体
app.post('/data', (req, res) => {
    const { name, email } = req.body;
    res.json({ received: { name, email } });
});

// 路径参数
app.get('/users/:id/posts/:postId', (req, res) => {
    const { id, postId } = req.params;
    res.json({ userId: id, postId });
});

// 响应方法
res.json({ data: 'json' });
res.status(201).json({ created: true });
res.send('text response');
res.redirect('/new-url');
res.download('./file.pdf');
```

### 五、错误处理

```javascript
// 异步错误处理
const asyncHandler = (fn) => (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
};

app.get('/users', asyncHandler(async (req, res) => {
    const users = await User.find();
    res.json(users);
}));

// 自定义错误类
class AppError extends Error {
    constructor(message, statusCode) {
        super(message);
        this.statusCode = statusCode;
        this.isOperational = true;
    }
}

// 使用
app.get('/users/:id', asyncHandler(async (req, res, next) => {
    const user = await User.findById(req.params.id);
    if (!user) {
        return next(new AppError('User not found', 404));
    }
    res.json(user);
}));
```

### 六、静态文件与模板

```javascript
// 静态文件
app.use(express.static('public'));
app.use('/uploads', express.static('uploads'));

// EJS模板
app.set('view engine', 'ejs');
app.set('views', './views');

app.get('/', (req, res) => {
    res.render('index', { title: 'Home', users });
});
```
