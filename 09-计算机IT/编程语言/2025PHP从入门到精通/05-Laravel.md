# Laravel

## Laravel基础架构
- Laravel：最流行的PHP框架，优雅的语法，丰富的功能生态
- 核心特性：路由、中间件、Eloquent ORM、Blade模板、Artisan命令行、队列
- 目录结构：app（应用代码）、routes（路由定义）、resources（视图）、config（配置）、database（迁移和种子）
- 安装：`composer create-project laravel/laravel project`
- 环境配置：`.env` 文件管理数据库、缓存、队列等配置
- 服务容器：Laravel的核心，依赖注入和IoC容器

## 路由与控制器
- 路由定义：`Route::get('/users', [UserController::class, 'index'])`
- 路由方法：get、post、put、patch、delete、any、match
- 路由参数：`Route::get('/users/{id}', function($id) {})`，`{id?}` 可选参数
- 路由分组：`Route::prefix('api')->middleware('auth')->group(function() { ... })`
- 命名路由：`Route::get('/users', ...)->name('users.index')`
- 资源路由：`Route::resource('users', UserController::class)` 自动生成CRUD路由
- 控制器：`php artisan make:controller UserController --resource`

## 中间件与认证
- 中间件：请求到达控制器前/后的处理层，如认证、日志、CORS
- 创建中间件：`php artisan make:middleware CheckAge`
- 注册：全局中间件（Kernel.php）、路由中间件（指定路由）
- 内置中间件：auth、guest、throttle（限流）、verified（邮箱验证）
- 认证系统：`php artisan make:auth` 生成认证脚手架
- Sanctum：API Token认证、SPA认证
- Guard：定义认证方式（session、token）
- 策略（Policy）：授权逻辑，`UserPolicy` 控制用户对资源的访问

## Eloquent ORM
- 模型：`class User extends Model { protected $fillable = ['name', 'email']; }`
- CRUD：`User::create($data)`、`User::find($id)`、`$user->update($data)`、`$user->delete()`
- 查询构建器：`User::where('age', '>', 18)->orderBy('name')->paginate(10)`
- 关联关系：hasOne、hasMany、belongsTo、belongsToMany（多对多）
- 预加载：`User::with('posts')->get()` 避免N+1查询问题
- 软删除：`use SoftDeletes;` 逻辑删除而非物理删除
- 访问器与修改器：`getFullNameAttribute()`、`setPasswordAttribute()`
- 作用域：`scope` 方法定义常用查询条件

## 数据库迁移与模板
- 迁移（Migration）：版本控制数据库结构
- 创建迁移：`php artisan create:migration create_users_table`
- Schema构建器：`Schema::create('users', function(Blueprint $table) { $table->id(); $table->string('name'); })`
- 回滚：`php artisan migrate:rollback`
- 种子（Seeder）：填充测试数据，`php artisan db:seed`
- 工厂（Factory）：模型工厂批量创建测试数据
- Blade模板：`@if`、`@foreach`、`@section`、`@yield`、`@extends`、`@include`
- 组件：`<x-alert type="warning">Message</x-alert>` Blade组件
