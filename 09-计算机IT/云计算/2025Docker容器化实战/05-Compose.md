# Docker Compose


## 收集指南

> ⚠️ **严格范围限定：** 仅收集本章（第5章 Compose）相关内容，禁止跨章节引用。

### 条目描述
本文件是《2025Docker容器化实战》中关于「Compose」的知识原子文件，属于云计算方向。

### 知识结构
- Compose 基础
- 服务编排
- 网络配置
- 卷管理
- 生产环境部署

### 待收集原子知识点
- docker-compose.yml 语法
- 服务依赖与启动顺序
- 自定义网络
- 持久化卷
- 环境变量与配置管理

## 核心知识点

### 一、Compose 文件基础

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8080:8000"
    environment:
      - APP_ENV=production
      - DB_HOST=db
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    volumes:
      - static_files:/app/static
    restart: unless-stopped
    networks:
      - frontend
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_password
      MYSQL_DATABASE: myapp
    volumes:
      - mysql_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"
    networks:
      - backend
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    secrets:
      - db_root_password

  cache:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_files:/usr/share/nginx/html/static
    depends_on:
      - web
    networks:
      - frontend

volumes:
  mysql_data:
  redis_data:
  static_files:

networks:
  frontend:
  backend:

secrets:
  db_root_password:
    file: ./secrets/db_password.txt
```

### 二、Compose 常用命令

```bash
# 启动所有服务
docker compose up -d

# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f web
docker compose logs --tail 100

# 停止并删除
docker compose down
docker compose down -v  # 同时删除卷

# 重新构建并启动
docker compose up -d --build

# 扩展服务实例
docker compose up -d --scale web=3

# 执行一次性命令
docker compose exec web python manage.py migrate
docker compose run --rm web python manage.py test

# 查看服务配置
docker compose config
```

### 三、服务依赖与健康检查

```yaml
services:
  web:
    depends_on:
      db:
        condition: service_healthy    # 等待健康检查通过
      redis:
        condition: service_started    # 等待服务启动
```

- **启动顺序控制：**
  - `service_started`：服务启动后（不保证就绪）
  - `service_healthy`：健康检查通过后（推荐）
  - `service_completed_successfully`：服务执行完成后

### 四、环境变量管理

```bash
# .env 文件
DB_PASSWORD=secretpassword
APP_PORT=8080
```

```yaml
# docker-compose.yml 引用 .env
services:
  web:
    ports:
      - "${APP_PORT}:8000"
    environment:
      DB_PASSWORD: ${DB_PASSWORD}

# 使用 env_file
services:
  web:
    env_file:
      - .env
      - .env.production
```

### 五、生产环境最佳实践

- **镜像版本锁定：** 使用具体版本号而非 `latest`
- **资源限制：**
  ```yaml
  services:
    web:
      deploy:
        resources:
          limits:
            cpus: '1.0'
            memory: 512M
          reservations:
            memory: 256M
  ```
- **日志管理：** 配置日志驱动和轮转
- **健康检查：** 所有服务都配置健康检查
- **Secrets：** 使用 Docker Secrets 管理敏感信息
- **重启策略：** `restart: unless-stopped`
