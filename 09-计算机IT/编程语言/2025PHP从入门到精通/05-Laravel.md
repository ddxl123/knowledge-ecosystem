# Laravel框架

## 核心知识点

### 一、路由

#### 1. 基本路由
```php
// routes/web.php
Route::get('/', function () {
    return view('welcome');
});

Route::get('/users', [UserController::class, 'index']);
Route::post('/users', [UserController::class, 'store']);
Route::get('/users/{user}', [UserController::class, 'show']);
Route::put('/users/{user}', [UserController::class, 'update']);
Route::delete('/users/{user}', [UserController::class, 'destroy']);
```

#### 2. 路由组
```php
Route::prefix('api/v1')->group(function () {
    Route::apiResource('users', UserController::class);
    Route::apiResource('posts', PostController::class);
});

Route::middleware(['auth'])->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index']);
    Route::get('/profile', [ProfileController::class, 'edit']);
});
```

### 二、控制器

```php
class UserController extends Controller {
    public function index() {
        $users = User::all();
        return view('users.index', compact('users'));
    }

    public function store(Request $request) {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|email|unique:users',
            'password' => 'required|min:8|confirmed',
        ]);

        $user = User::create($validated);
        return redirect()->route('users.show', $user);
    }

    public function show(User $user) {
        return view('users.show', compact('user'));
    }
}
```

### 三、Eloquent ORM

#### 1. 模型定义
```php
class User extends Model {
    use HasFactory, SoftDeletes;

    protected $fillable = ['name', 'email', 'password'];
    protected $hidden = ['password', 'remember_token'];
    protected $casts = [
        'email_verified_at' => 'datetime',
        'password' => 'hashed',
    ];

    // 关联
    public function posts() {
        return $this->hasMany(Post::class);
    }

    public function profile() {
        return $this->hasOne(Profile::class);
    }

    public function roles() {
        return $this->belongsToMany(Role::class);
    }
}
```

#### 2. 查询构建器
```php
// 基本查询
$users = User::where('active', true)
    ->orderBy('name')
    ->limit(10)
    ->get();

// 分页
$users = User::paginate(15);

// 聚合
$count = User::where('active', true)->count();
$avg = User::avg('age');

// 创建
$user = User::create(['name' => 'Alice', 'email' => 'alice@example.com']);

// 更新
$user->update(['name' => 'Bob']);

// 删除
$user->delete();
```

### 四、Blade模板

```php
{{-- layout.blade.php --}}
<!DOCTYPE html>
<html>
<head>
    <title>@yield('title', 'My App')</title>
</head>
<body>
    @include('partials.nav')

    <div class="container">
        @yield('content')
    </div>

    @stack('scripts')
</body>
</html>

{{-- users/index.blade.php --}}
@extends('layout')

@section('title', 'Users')

@section('content')
    <h1>Users</h1>

    @forelse($users as $user)
        <div class="user">
            <h2>{{ $user->name }}</h2>
            <p>{{ $user->email }}</p>
        </div>
    @empty
        <p>No users found.</p>
    @endforelse

    {{ $users->links() }}
@endsection
```

### 五、中间件

```php
class EnsureIsAdmin {
    public function handle(Request $request, Closure $next) {
        if (!$request->user() || !$request->user()->is_admin) {
            abort(403, 'Unauthorized');
        }
        return $next($request);
    }
}

// 注册使用
Route::middleware(['auth', 'admin'])->group(function () {
    Route::get('/admin', [AdminController::class, 'index']);
});
```

### 六、表单请求验证

```php
class StoreUserRequest extends FormRequest {
    public function authorize(): bool {
        return true;
    }

    public function rules(): array {
        return [
            'name' => 'required|string|max:255',
            'email' => 'required|email|unique:users',
            'password' => 'required|min:8|confirmed',
        ];
    }

    public function messages(): array {
        return [
            'email.unique' => '该邮箱已被注册',
            'password.min' => '密码至少需要8个字符',
        ];
    }
}
```
