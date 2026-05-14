# Spring Boot REST（2026版）


## 收集指南

> ⚠️ **严格范围限定：** 仅收集本章（第4章 REST）相关内容，禁止跨章节引用。

### 条目描述
本文件是《2026Spring Boot实战》中关于「REST」的知识原子文件，属于后端开发方向。

### 知识结构
- RESTful API 2026 设计趋势
- HTTP 接口声明式客户端
- GraphQL 集成
- API 网关集成
- 性能与缓存

### 待收集原子知识点
- 现代 API 设计规范
- 声明式 HTTP 客户端
- GraphQL vs REST
- API 网关模式
- 响应缓存策略

## 核心知识点

### 一、声明式 HTTP 客户端

```java
// 声明式 HTTP 接口（Spring 6.x+）
@HttpExchange(url = "/api/v1/users", accept = MediaType.APPLICATION_JSON_VALUE)
public interface UserHttpClient {
    
    @GetExchange("/{id}")
    UserDTO getById(@PathVariable Long id);
    
    @GetExchange
    Page<UserDTO> list(@RequestParam int page, @RequestParam int size);
    
    @PostExchange
    UserDTO create(@RequestBody UserCreateRequest request);
    
    @PutExchange("/{id}")
    UserDTO update(@PathVariable Long id, @RequestBody UserUpdateRequest request);
    
    @DeleteExchange("/{id}")
    void delete(@PathVariable Long id);
}

// 配置与注入
@Configuration
public class HttpClientConfig {
    @Bean
    public UserHttpClient userHttpClient(HttpClientProperties properties) {
        RestClient restClient = RestClient.builder()
            .baseUrl(properties.getUserServiceUrl())
            .requestInterceptor(new LoggingInterceptor())
            .build();
        HttpServiceProxyFactory factory = HttpServiceProxyFactory
            .builderFor(RestClientAdapter.create(restClient))
            .build();
        return factory.createClient(UserHttpClient.class);
    }
}
```

### 二、RestClient 新一代 HTTP 客户端

```java
// RestClient（替代 RestTemplate）
@Service
public class ExternalApiService {
    private final RestClient restClient;
    
    public ExternalApiService(RestClient.Builder builder) {
        this.restClient = builder
            .baseUrl("https://api.external.com")
            .defaultHeader("Authorization", "Bearer " + token)
            .build();
    }
    
    public ExternalUser getExternalUser(String id) {
        return restClient.get()
            .uri("/users/{id}", id)
            .retrieve()
            .body(ExternalUser.class);
    }
    
    public ExternalUser createExternalUser(CreateRequest request) {
        return restClient.post()
            .uri("/users")
            .contentType(MediaType.APPLICATION_JSON)
            .body(request)
            .retrieve()
            .onStatus(HttpStatusCode::is4xxClientError, (req, resp) -> {
                throw new ExternalApiException(resp.getStatusCode().value());
            })
            .body(ExternalUser.class);
    }
}
```

### 三、GraphQL 集成

```java
// Spring for GraphQL
@Controller
public class UserGraphQLController {
    
    @Autowired
    private UserService userService;
    
    @QueryMapping
    public User userById(@Argument Long id) {
        return userService.findById(id);
    }
    
    @QueryMapping
    public List<User> users(@Argument int page, @Argument int size) {
        return userService.findAll(PageRequest.of(page, size));
    }
    
    @MutationMapping
    public User createUser(@Argument UserInput input) {
        return userService.create(input);
    }
    
    @SchemaMapping(typeName = "User", field = "orders")
    public List<Order> orders(User user) {
        return orderService.findByUserId(user.getId());
    }
}

// GraphQL Schema（schema.graphqls）
type User {
    id: ID!
    username: String!
    email: String!
    orders: [Order!]!
}
```

### 四、API 版本与协商

```java
// 内容协商版本控制
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @GetMapping(value = "/{id}", produces = "application/vnd.myapp.v1+json")
    public UserV1 getByIdV1(@PathVariable Long id) {
        return userService.findByIdV1(id);
    }
    
    @GetMapping(value = "/{id}", produces = "application/vnd.myapp.v2+json")
    public UserV2 getByIdV2(@PathVariable Long id) {
        return userService.findByIdV2(id);
    }
}

// 响应式流式 API
@GetMapping(value = "/stream", produces = MediaType.APPLICATION_NDJSON_VALUE)
public Flux<UserDTO> streamUsers() {
    return userService.streamAll()
        .delayElements(Duration.ofMillis(100));
}
```

### 五、响应缓存策略

```java
// HTTP 缓存控制
@GetMapping("/{id}")
public ResponseEntity<UserDTO> getById(@PathVariable Long id) {
    UserDTO user = userService.findById(id);
    return ResponseEntity.ok()
        .cacheControl(CacheControl.maxAge(Duration.ofMinutes(10))
            .mustRevalidate())
        .eTag(String.valueOf(user.hashCode()))
        .lastModified(user.getUpdatedAt())
        .body(user);
}

// 条件请求（If-None-Match / If-Modified-Since）
@GetMapping("/{id}")
public ResponseEntity<UserDTO> getById(
        @PathVariable Long id,
        @RequestHeader(value = "If-None-Match", required = false) String ifNoneMatch) {
    UserDTO user = userService.findById(id);
    String etag = "\"" + user.hashCode() + "\"";
    
    if (etag.equals(ifNoneMatch)) {
        return ResponseEntity.status(304).build();
    }
    return ResponseEntity.ok().eTag(etag).body(user);
}
```
