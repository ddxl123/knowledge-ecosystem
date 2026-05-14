# Web开发

## HTTP服务器
- 标准库http：`http.ListenAndServe(":8080", mux)` 即可启动服务器
- 路由多路复用器：http.ServeMux，Go 1.22+支持方法匹配 `mux.HandleFunc("GET /api/users", handler)`
- 中间件模式：函数接受Handler返回Handler，实现日志、认证、CORS等
- 中间件链：`func chain(h http.Handler, middlewares ...Middleware) http.Handler`
- Graceful Shutdown：`server.Shutdown(ctx)` 优雅关闭，等待请求完成
- http.Server配置：ReadTimeout、WriteTimeout、IdleTimeout、MaxHeaderBytes

## Gin框架
- 路由：`r := gin.Default(); r.GET("/users", handler)` RESTful风格路由
- 路由分组：`v1 := r.Group("/api/v1")` 统一前缀和中间件
- 路径参数：`c.Param("id")` 获取URL中的参数
- 查询参数：`c.Query("page")` 获取查询字符串
- 请求绑定：`c.ShouldBindJSON(&user)` 自动解析请求体到结构体
- 响应：`c.JSON(200, gin.H{"message": "ok"})` 返回JSON
- 中间件：`r.Use(middleware)` 全局中间件
- 自定义中间件：`func AuthMiddleware() gin.HandlerFunc { return func(c *gin.Context) {...} }`

## 模板渲染
- html/template：Go标准库模板引擎，自动HTML转义防XSS
- 模板语法：`{{.Field}}` 输出字段、`{{if .Condition}}...{{end}}` 条件、`{{range .Items}}...{{end}}` 循环
- 模板函数：`{{FuncName .Arg}}` 自定义模板函数
- 模板继承：`{{define "layout"}}` 定义布局、`{{template "content" .}}` 嵌入
- Gin模板：`r.LoadHTMLGlob("templates/*"); c.HTML(200, "index.html", data)`
- 静态文件：`r.Static("/static", "./static")` 提供静态资源服务

## 数据库操作
- database/sql：标准库SQL接口，需配合驱动（如go-sql-driver/mysql）
- 连接：`sql.Open("mysql", "user:pass@tcp(host:port)/dbname")`
- 查询：`db.Query("SELECT * FROM users WHERE id = ?", id)` 返回Rows
- 单行查询：`db.QueryRow("SELECT name FROM users WHERE id = ?", id).Scan(&name)`
- 增删改：`db.Exec("INSERT INTO users (name) VALUES (?)", name)`
- 事务：`tx, _ := db.Begin(); tx.Exec(...); tx.Commit()`
- 连接池：`db.SetMaxOpenConns(25); db.SetMaxIdleConns(5)`
- GORM：Go最流行的ORM库，自动迁移、关联查询、钩子函数

## RESTful API设计
- 资源命名：使用名词复数（/users、/orders），避免动词
- HTTP方法语义：GET查询、POST创建、PUT全量更新、PATCH部分更新、DELETE删除
- 状态码：200成功、201已创建、204无内容、400客户端错误、401未认证、403禁止、404未找到、500服务器错误
- 版本控制：URL路径（/api/v1/users）或请求头（Accept-Version）
- 分页：`?page=1&pageSize=20`，返回总数和分页信息
- 错误响应：统一格式 `{"code": 400, "message": "invalid parameter"}`
- JWT认证：`github.com/golang-jwt/jwt` 生成和验证Token
