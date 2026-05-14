# Django REST Framework


## 收集指南

> ⚠️ **严格范围限定：** 仅收集本章（第5章 REST）相关内容，禁止跨章节引用。

### 条目描述
本文件是《2025Django实战》中关于「REST」的知识原子文件，属于后端开发方向。

### 知识结构
- DRF 序列化器
- 视图集与路由
- 认证与权限
- 分页与过滤
- API 文档

### 待收集原子知识点
- Serializer 与 ModelSerializer
- ViewSet 与 Router
- 认证、权限、节流
- 分页、过滤、搜索
- Swagger/OpenAPI 文档

## 核心知识点

### 一、序列化器（Serializer）

```python
from rest_framework import serializers
from .models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author_name', 'created_at']
        read_only_fields = ['created_at']

class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author_name', 'tags', 
                  'comments', 'comments_count', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError('标题至少5个字符')
        return value

# 嵌套创建
class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'tags', 'status']
    
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        article = Article.objects.create(**validated_data)
        article.tags.set(tags)
        return article
```

### 二、视图集与路由

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filterset_fields = ['status', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ArticleCreateSerializer
        return ArticleSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    # 自定义 action
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        article = self.get_object()
        article.status = 'published'
        article.save()
        return Response({'status': 'published'})
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured = self.queryset.filter(is_featured=True)[:10]
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)

# 路由配置
router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

### 三、认证与权限

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return obj.author == request.user

class ArticleViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    
    # 按 action 设置不同权限
    def get_permissions(self):
        if self.action == 'list':
            return []  # 公开访问
        if self.action in ('create',):
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAuthorOrReadOnly()]
```

- **DRF 内置权限：**
  - `AllowAny`：允许所有请求
  - `IsAuthenticated`：需登录
  - `IsAdminUser`：需管理员
  - `IsAuthenticatedOrReadOnly`：登录用户可写，匿名可读

### 四、分页与过滤

```python
# settings.py 全局配置
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# 自定义分页
class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# 使用 django-filter
import django_filters

class ArticleFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Article
        fields = ['status', 'author', 'category']
```

### 五、API 文档（drf-spectacular）

```python
# settings.py
INSTALLED_APPS += ['drf_spectacular']

REST_FRAMEWORK['DEFAULT_SCHEMA_CLASS'] = 'drf_spectacular.openapi.AutoSchema'

SPECTACULAR_SETTINGS = {
    'TITLE': '文章管理系统 API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# urls.py
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```
