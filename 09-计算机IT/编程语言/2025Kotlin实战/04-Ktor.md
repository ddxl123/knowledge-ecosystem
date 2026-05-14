# Ktor

## Ktor基础
- Ktor：JetBrains开发的Kotlin异步Web框架，基于协程
- 服务器和客户端：Ktor同时提供服务器端和HTTP客户端框架
- 轻量级：核心功能小，通过插件（Plugin）按需扩展
- 嵌入式服务器：可嵌入到任何Kotlin应用中
- 安装：Gradle依赖引入`io.ktor:ktor-server-core`等模块

## 服务器端
- 创建服务器：`embeddedServer(Netty, port = 8080) { configureRouting() }.start(wait = true)`
- 路由定义：
  ```kotlin
  routing {
      get("/users") { call.respondText("User list") }
      post("/users") { val user = call.receive<User>() }
      get("/users/{id}") { val id = call.parameters["id"] }
  }
  ```
- 路由分组：`route("/api/v1") { get("/users") {...} }`
- 响应类型：respondText、respond、respondBytes、respondRedirect
- 内容协商：自动根据Accept头选择JSON/XML等格式响应

## 插件系统
- 安装插件：`install(ContentNegotiation) { json() }`
- ContentNegotiation：自动序列化/反序列化请求和响应体（JSON/XML）
- Authentication：身份验证插件，支持JWT、OAuth、Session等
- CORS：跨域资源共享配置
- StatusPages：统一异常处理，`exception<NotFoundException> { call.respond(HttpStatusCode.NotFound) }`
- 自定义插件：`val MyPlugin = createApplicationPlugin(name = "MyPlugin") { ... }`
- 日志：Logging插件记录请求和响应
- 压缩：Compression插件压缩响应体

## HTTP客户端
- 创建客户端：`val client = HttpClient(CIO) { install(ContentNegotiation) { json() } }`
- GET请求：`client.get("https://api.example.com/users")`
- POST请求：`client.post("https://api.example.com/users") { setBody(user) }`
- 请求配置：headers、parameter、body、timeout
- 响应处理：`response.body<List<User>>()`
- 异常处理：`response.status` 检查状态码
- 引擎选择：CIO（纯Kotlin）、OkHttp、Java、Darwin（iOS）

## WebSocket与测试
- WebSocket服务端：`webSocket("/chat") { for (frame in incoming) { send(frame) } }`
- WebSocket客户端：`client.webSocket("/chat") { send("Hello"); for (frame in incoming) {...} }`
- 测试：`testApplication { client.get("/api/users").assertOk() }`
- 依赖注入：Koin或kodein集成
- 部署：Docker容器化、Fat JAR打包
- 性能：Ktor基于Netty，支持高并发连接
- 监控：Micrometer指标集成
