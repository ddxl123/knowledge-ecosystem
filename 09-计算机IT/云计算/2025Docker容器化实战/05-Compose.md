# Docker Compose

## 核心知识点

### 一、基本配置

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### 二、常用命令

```bash
# 启动服务
docker compose up -d

# 停止服务
docker compose down

# 查看状态
docker compose ps

# 查看日志
docker compose logs -f web

# 重建服务
docker compose up -d --build

# 扩展服务
docker compose up -d --scale web=3

# 执行命令
docker compose exec web bash
docker compose exec db psql -U user mydb
```

### 三、环境变量

```yaml
services:
  web:
    image: myapp
    env_file:
      - .env
    environment:
      - NODE_ENV=${NODE_ENV:-production}
      - SECRET_KEY=${SECRET_KEY}
```

```bash
# .env文件
NODE_ENV=production
SECRET_KEY=my-secret-key
DB_PASSWORD=secure-password
```

### 四、健康检查

```yaml
services:
  web:
    build: .
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### 五、网络配置

```yaml
services:
  web:
    networks:
      - frontend
      - backend

  api:
    networks:
      - backend

  db:
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # 不允许外部访问
```

### 六、多环境配置

```yaml
# docker-compose.yml（基础配置）
services:
  web:
    build: .

# docker-compose.override.yml（开发环境，自动加载）
services:
  web:
    ports:
      - "3000:3000"
    volumes:
      - ./src:/app/src

# docker-compose.prod.yml（生产环境）
services:
  web:
    restart: unless-stopped
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
```

```bash
# 使用生产配置
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
