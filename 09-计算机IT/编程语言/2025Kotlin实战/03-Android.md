# Android开发

## Activity与生命周期
- Activity：Android四大组件之一，代表一个用户界面
- 生命周期：onCreate → onStart → onResume → onPause → onStop → onDestroy
- 重建：配置变更（如旋转屏幕）会销毁重建Activity
- 保存状态：onSaveInstanceState()保存、onRestoreInstanceState()恢复
- Intent：组件间通信，显式Intent指定目标组件、隐式Intent通过Action匹配
- Activity启动模式：standard、singleTop、singleTask、singleInstance

## Jetpack Compose
- 声明式UI：用Kotlin代码描述界面，替代XML布局
- Composable函数：`@Composable fun Greeting(name: String) { Text("Hello $name") }`
- 状态管理：`remember { mutableStateOf(0) }` 保存可变状态
- 重组（Recomposition）：状态变化时自动重新调用受影响的Composable
- Material Design组件：Scaffold、TopAppBar、BottomNavigation、FloatingActionButton
- 列表：`LazyColumn { items(list) { item -> ... } }`
- 导航：NavHost + NavController，声明式导航图

## ViewModel与LiveData
- ViewModel：管理UI相关数据，配置变更时存活
- 创建：`class MyViewModel : ViewModel() { val data = MutableLiveData<String>() }`
- LiveData：可观察的数据持有者，生命周期感知，自动取消订阅
- MutableLiveData：可变版本，ViewModel内部使用
- 对外暴露：`val data: LiveData<String> = _data` 只读LiveData
- Transformations：map()、switchMap() 转换LiveData
- ViewModelProvider：`ViewModelProvider(this)[MyViewModel::class.java]`

## 数据持久化
- Room数据库：SQLite的抽象层，编译时验证SQL
- Entity：`@Entity data class User(@PrimaryKey val id: Int, val name: String)`
- DAO：`@Dao interface UserDao { @Query("SELECT * FROM user") fun getAll(): Flow<List<User>> }`
- Database：`@Database(entities = [User::class], version = 1) abstract class AppDatabase : RoomDatabase()`
- DataStore：替代SharedPreferences，支持类型安全
- Proto DataStore：使用Protocol Buffers定义数据结构
- 文件存储：内部存储（应用私有）、外部存储（需权限）

## 网络与依赖注入
- Retrofit：类型安全的HTTP客户端，`@GET("users/{id}") suspend fun getUser(@Path("id") id: Int): User`
- OkHttp：底层HTTP客户端，Retrofit默认使用
- Moshi/Gson：JSON序列化/反序列化
- Hilt：Dagger的简化版依赖注入框架，`@HiltAndroidApp`、`@Inject`、`@Module`
- WorkManager：可靠的后台任务调度，支持约束条件和链式任务
- 权限：AndroidManifest声明 + 运行时请求（ActivityResultContracts）
