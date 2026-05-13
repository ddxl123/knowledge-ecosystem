# Ktor框架

## 核心知识点

### 一、基本服务器

```kotlin
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.ktor.server.application.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

fun main() {
    embeddedServer(Netty, port = 8080) {
        routing {
            get("/") {
                call.respondText("Hello, Ktor!")
            }
            get("/json") {
                call.respond(mapOf("message" to "Hello", "status" to "ok"))
            }
        }
    }.start(wait = true)
}
```

### 二、路由

```kotlin
fun Application.configureRouting() {
    routing {
        // 基本路由
        get("/users") {
            call.respond(users)
        }

        // 路径参数
        get("/users/{id}") {
            val id = call.parameters["id"]?.toIntOrNull()
            val user = users.find { it.id == id }
            if (user != null) {
                call.respond(user)
            } else {
                call.respond(HttpStatusCode.NotFound, "User not found")
            }
        }

        // 路由组
        route("/api/v1") {
            get("/users") { /* ... */ }
            post("/users") { /* ... */ }
            put("/users/{id}") { /* ... */ }
            delete("/users/{id}") { /* ... */ }
        }
    }
}
```

### 三、请求处理

```kotlin
// POST请求与JSON解析
@Serializable
data class CreateUserRequest(val name: String, val email: String)

fun Application.configureSerialization() {
    install(ContentNegotiation) {
        json()
    }
}

routing {
    post("/users") {
        val request = call.receive<CreateUserRequest>()
        val user = User(id = nextId++, name = request.name, email = request.email)
        users.add(user)
        call.respond(HttpStatusCode.Created, user)
    }
}

// 查询参数
get("/search") {
    val query = call.request.queryParameters["q"] ?: ""
    val limit = call.request.queryParameters["limit"]?.toIntOrNull() ?: 10
    // 搜索逻辑...
}
```

### 四、中间件与插件

```kotlin
// 日志插件
install(CallLogging) {
    level = Level.INFO
}

// CORS插件
install(CORS) {
    anyHost()
    allowHeader(HttpHeaders.ContentType)
}

// 认证插件
install(Authentication) {
    basic("auth-basic") {
        realm = "Ktor Server"
        validate { credentials ->
            if (credentials.name == "admin" && credentials.password == "password") {
                UserIdPrincipal(credentials.name)
            } else {
                null
            }
        }
    }

    jwt("auth-jwt") {
        realm = "Ktor Server"
        verifier(JWT.require(Algorithm.HMAC256("secret")).build())
        validate { credential ->
            if (credential.payload.subject != null) {
                JWTPrincipal(credential.payload)
            } else {
                null
            }
        }
    }
}

// 使用认证
routing {
    authenticate("auth-jwt") {
        get("/protected") {
            val principal = call.principal<JWTPrincipal>()
            call.respondText("Hello, ${principal!!.payload.subject}")
        }
    }
}
```

### 五、WebSocket

```kotlin
install(WebSockets)

routing {
    webSocket("/chat") {
        send("Connected to chat")

        for (frame in incoming) {
            when (frame) {
                is Frame.Text -> {
                    val text = frame.readText()
                    send("Echo: $text")
                }
                else -> {}
            }
        }
    }
}
```

### 六、测试

```kotlin
class ApplicationTest {
    @Test
    fun testRoot() = testApplication {
        application {
            configureRouting()
        }

        client.get("/").apply {
            assertEquals(HttpStatusCode.OK, status)
            assertEquals("Hello, Ktor!", bodyAsText())
        }
    }

    @Test
    fun testCreateUser() = testApplication {
        application {
            configureRouting()
            configureSerialization()
        }

        val response = client.post("/users") {
            contentType(ContentType.Application.Json)
            setBody(CreateUserRequest("Alice", "alice@example.com"))
        }

        assertEquals(HttpStatusCode.Created, response.status)
    }
}
```
