# Web开发

## 核心知识点

### 一、net/http标准库

#### 1. 基本服务器
```go
func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/", homeHandler)
    mux.HandleFunc("/api/users", usersHandler)

    server := &http.Server{
        Addr:         ":8080",
        Handler:      mux,
        ReadTimeout:  10 * time.Second,
        WriteTimeout: 10 * time.Second,
    }

    log.Fatal(server.ListenAndServe())
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Welcome to Go Web")
}
```

#### 2. 请求处理
```go
func usersHandler(w http.ResponseWriter, r *http.Request) {
    switch r.Method {
    case http.MethodGet:
        // 获取用户列表
        json.NewEncoder(w).Encode(users)
    case http.MethodPost:
        // 创建用户
        var user User
        json.NewDecoder(r.Body).Decode(&user)
        // 保存用户...
        w.WriteHeader(http.StatusCreated)
    default:
        w.WriteHeader(http.StatusMethodNotAllowed)
    }
}
```

### 二、Gin框架

#### 1. 基本使用
```go
r := gin.Default()

r.GET("/ping", func(c *gin.Context) {
    c.JSON(200, gin.H{"message": "pong"})
})

r.Run(":8080")
```

#### 2. 路由分组
```go
v1 := r.Group("/api/v1")
{
    v1.GET("/users", getUsers)
    v1.POST("/users", createUser)
    v1.GET("/users/:id", getUser)
    v1.PUT("/users/:id", updateUser)
    v1.DELETE("/users/:id", deleteUser)
}
```

#### 3. 参数绑定
```go
type LoginForm struct {
    User     string `form:"user" binding:"required"`
    Password string `form:"password" binding:"required"`
}

func login(c *gin.Context) {
    var form LoginForm
    if err := c.ShouldBind(&form); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
    c.JSON(200, gin.H{"status": "logged in"})
}
```

### 三、中间件

#### 1. 自定义中间件
```go
func Logger() gin.HandlerFunc {
    return func(c *gin.Context) {
        t := time.Now()
        c.Next()
        latency := time.Since(t)
        log.Printf("[%s] %s %v", c.Request.Method, c.Request.URL.Path, latency)
    }
}

func AuthRequired() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.AbortWithStatusJSON(401, gin.H{"error": "unauthorized"})
            return
        }
        // 验证token...
        c.Next()
    }
}
```

#### 2. 使用中间件
```go
r := gin.Default()
r.Use(Logger())

authorized := r.Group("/admin")
authorized.Use(AuthRequired())
{
    authorized.GET("/dashboard", dashboardHandler)
}
```

### 四、模板渲染

```go
r := gin.Default()
r.LoadHTMLGlob("templates/*")

r.GET("/index", func(c *gin.Context) {
    c.HTML(200, "index.html", gin.H{
        "title": "Go Web App",
        "user":  "Alice",
    })
})
```

### 五、数据库操作

```go
// 使用database/sql
import _ "github.com/go-sql-driver/mysql"

db, err := sql.Open("mysql", "user:password@tcp(127.0.0.1:3306)/mydb")
if err != nil {
    log.Fatal(err)
}
defer db.Close()

// 查询
rows, err := db.Query("SELECT id, name FROM users WHERE age > ?", 18)
for rows.Next() {
    var id int
    var name string
    rows.Scan(&id, &name)
    fmt.Println(id, name)
}

// 插入
result, err := db.Exec("INSERT INTO users (name, age) VALUES (?, ?)", "Bob", 25)
id, _ := result.LastInsertId()
```
