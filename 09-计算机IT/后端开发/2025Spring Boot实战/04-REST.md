# Spring Boot REST API


## 收集指南

> ⚠️ **严格范围限定：** 仅收集本章（第4章 REST）相关内容，禁止跨章节引用。

### 条目描述
本文件是《2025Spring Boot实战》中关于「REST API」的知识原子文件，属于后端开发方向。

### 知识结构
- RESTful API 设计原则
- 请求与响应处理
- 异常处理
- API 文档生成
- 版本控制

### 待收集原子知识点
- REST 架构风格与设计规范
- 请求参数绑定与响应封装
- 全局异常处理
- Swagger/OpenAPI 文档
- API 版本策略

## 核心知识点

### 一、RESTful API 设计原则

```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    // GET /api/v1/users - 列表查询
    @GetMapping
    public Page<UserDTO> list(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) String keyword) {
        return userService.search(keyword, PageRequest.of(page, size));
    }
    
    // GET /api/v1/users/{id} - 获取单个资源
    @GetMapping("/{id}")
    public UserDTO getById(@PathVariable Long id) {
        return userService.getById(id);
    }
    
    // POST /api/v1/users - 创建资源
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserDTO create(@Valid @RequestBody UserCreateRequest request) {
        return userService.create(request);
    }
    
    // PUT /api/v1/users/{id} - 全量更新
    @PutMapping("/{id}")
    public UserDTO update(@PathVariable Long id, @Valid @RequestBody UserUpdateRequest request) {
        return userService.update(id, request);
    }
    
    // DELETE /api/v1/users/{id} - 删除资源
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        userService.delete(id);
    }
}
```

- **REST 设计规范：**
  - URL 使用名词复数：`/users`、`/orders`
  - HTTP 方法语义化：GET 查询、POST 创建、PUT 更新、DELETE 删除
  - 状态码正确使用：200 成功、201 创建成功、204 无内容、400 请求错误、401 未认证、403 无权限、404 未找到
  - 嵌套资源：`/users/{id}/orders`

### 二、请求参数验证

```java
// 请求 DTO 验证
public class UserCreateRequest {
    @NotBlank(message = "用户名不能为空")
    @Size(min = 2, max = 50, message = "用户名长度2-50")
    private String username;
    
    @NotBlank @Email(message = "邮箱格式不正确")
    private String email;
    
    @NotNull @Min(0) @Max(150)
    private Integer age;
    
    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
    private String phone;
}

// 全局异常处理
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
        Map<String, String> errors = ex.getBindingResult().getFieldErrors().stream()
            .collect(Collectors.toMap(
                FieldError::getField, 
                fe -> Optional.ofNullable(fe.getDefaultMessage()).orElse("")));
        return ResponseEntity.badRequest().body(new ErrorResponse(400, "参数验证失败", errors));
    }
    
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        return ResponseEntity.status(404).body(new ErrorResponse(404, ex.getMessage(), null));
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneral(Exception ex) {
        return ResponseEntity.status(500).body(new ErrorResponse(500, "服务器内部错误", null));
    }
}
```

### 三、统一响应封装

```java
// 统一响应体
public class ApiResponse<T> {
    private int code;
    private String message;
    private T data;
    private long timestamp;
    
    public static <T> ApiResponse<T> success(T data) {
        return new ApiResponse<>(200, "success", data, System.currentTimeMillis());
    }
    
    public static <T> ApiResponse<T> error(int code, String message) {
        return new ApiResponse<>(code, message, null, System.currentTimeMillis());
    }
}

// 响应实体包装
@GetMapping("/{id}")
public ApiResponse<UserDTO> getById(@PathVariable Long id) {
    return ApiResponse.success(userService.getById(id));
}
```

### 四、Swagger/OpenAPI 文档

```java
// OpenAPI 3.0 配置
@Configuration
public class OpenApiConfig {
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("用户管理 API")
                .version("1.0")
                .description("用户管理系统接口文档"))
            .addSecurityItem(new SecurityRequirement().addList("Bearer"))
            .components(new Components()
                .addSecuritySchemes("Bearer",
                    new SecurityScheme()
                        .type(SecurityScheme.Type.HTTP)
                        .scheme("bearer")
                        .bearerFormat("JWT")));
    }
}

// Controller 文档注解
@Tag(name = "用户管理", description = "用户 CRUD 操作")
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    
    @Operation(summary = "获取用户详情", description = "根据ID查询用户信息")
    @ApiResponse(responseCode = "200", description = "查询成功")
    @ApiResponse(responseCode = "404", description = "用户不存在")
    @GetMapping("/{id}")
    public UserDTO getById(@Parameter(description = "用户ID") @PathVariable Long id) {
        return userService.getById(id);
    }
}
```

### 五、API 版本控制

```java
// URL 路径版本控制
@RestController
@RequestMapping("/api/v1/users")
public class UserControllerV1 { }

@RestController
@RequestMapping("/api/v2/users")
public class UserControllerV2 { }

// 请求头版本控制
@RestController
@RequestMapping("/api/users")
public class UserController {
    @GetMapping(headers = "X-API-VERSION=1")
    public UserV1 getV1() { }
    
    @GetMapping(headers = "X-API-VERSION=2")
    public UserV2 getV2() { }
}

// 媒体类型版本控制
@GetMapping(produces = "application/vnd.myapp.v1+json")
public UserV1 getV1() { }
```

- **版本控制策略选择：**
  - URL 路径版本：最直观，适合公共 API
  - 请求头版本：URL 保持简洁，适合内部 API
  - 媒体类型版本：最 RESTful，但使用复杂
