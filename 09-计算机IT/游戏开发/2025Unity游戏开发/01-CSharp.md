# Unity C# 编程


## 收集指南

> ⚠️ **严格范围限定：** 仅收集本章（第1章 C#）相关内容，禁止跨章节引用。

### 条目描述
本文件是《2025Unity游戏开发》中关于「C#」的知识原子文件，属于游戏开发方向。

### 知识结构
- C# 基础语法
- Unity 生命周期
- 面向对象编程
- 协程
- 委托与事件

### 待收集原子知识点
- 变量/类型/控制流
- MonoBehaviour 生命周期
- 继承与接口
- IEnumerator 协程
- Action/Func/事件系统

## 核心知识点

### 一、Unity C# 基础

```csharp
using UnityEngine;

public class Player : MonoBehaviour
{
    // 变量声明（Inspector 中可编辑）
    [SerializeField] private float speed = 5f;
    [SerializeField] private int health = 100;
    [SerializeField] private string playerName = "Hero";
    
    // 公开变量（Inspector 中可见）
    public GameObject bulletPrefab;
    public Transform firePoint;
    
    // 非序列化变量（Inspector 中不可见）
    private Rigidbody2D rb;
    private bool isGrounded;
    
    // 属性
    public int Health
    {
        get => health;
        set => health = Mathf.Clamp(value, 0, 100);
    }
    
    // 枚举
    public enum PlayerState { Idle, Running, Jumping, Attacking }
    private PlayerState currentState = PlayerState.Idle;
}
```

### 二、MonoBehaviour 生命周期

```csharp
public class GameManager : MonoBehaviour
{
    // 生命周期方法（按执行顺序）
    void Awake()         // 对象创建时（最早，适合初始化引用）
    {
        // 获取组件引用
        rb = GetComponent<Rigidbody2D>();
    }
    
    void OnEnable()      // 对象启用时
    {
        // 注册事件
    }
    
    void Start()         // 第一帧更新前（只执行一次）
    {
        // 初始化逻辑
    }
    
    void FixedUpdate()   // 固定时间间隔（默认0.02秒，物理计算）
    {
        // 物理移动、力的施加
        rb.velocity = new Vector2(horizontal * speed, rb.velocity.y);
    }
    
    void Update()        // 每帧调用（帧率不固定）
    {
        // 输入检测、游戏逻辑
        float horizontal = Input.GetAxis("Horizontal");
        if (Input.GetKeyDown(KeyCode.Space)) Jump();
    }
    
    void LateUpdate()    // Update 之后调用
    {
        // 摄像机跟随（确保在角色移动后更新）
        camera.transform.position = player.position + offset;
    }
    
    void OnDisable()     // 对象禁用时
    {
        // 取消事件注册
    }
    
    void OnDestroy()     // 对象销毁时
    {
        // 清理资源
    }
}
```

### 三、常用 Unity API

```csharp
// 组件获取
Rigidbody rb = GetComponent<Rigidbody>();
AudioSource audio = GetComponent<AudioSource>();
SpriteRenderer sprite = GetComponent<SpriteRenderer>();

// 查找对象
GameObject player = GameObject.Find("Player");
GameObject[] enemies = GameObject.FindGameObjectsWithTag("Enemy");
Camera mainCam = Camera.main;

// 变换操作
transform.position = new Vector3(1, 2, 0);
transform.rotation = Quaternion.Euler(0, 90, 0);
transform.localScale = Vector3.one * 2f;
transform.Translate(Vector3.forward * speed * Time.deltaTime);
transform.Rotate(Vector3.up, 90 * Time.deltaTime);

// 实例化与销毁
GameObject bullet = Instantiate(bulletPrefab, firePoint.position, firePoint.rotation);
Destroy(bullet, 3f); // 3秒后销毁

// 时间
Time.deltaTime       // 上一帧耗时（秒）
Time.time            // 游戏运行时间
Time.fixedDeltaTime  // FixedUpdate 间隔
```

### 四、协程（Coroutine）

```csharp
// 协程定义
IEnumerator DashCoroutine(float duration)
{
    float originalSpeed = speed;
    speed *= 2f;
    
    // 等待指定时间
    yield return new WaitForSeconds(duration);
    
    speed = originalSpeed;
}

IEnumerator FadeOut(Renderer renderer, float duration)
{
    Color color = renderer.material.color;
    float startAlpha = color.a;
    
    for (float t = 0; t < duration; t += Time.deltaTime)
    {
        color.a = Mathf.Lerp(startAlpha, 0, t / duration);
        renderer.material.color = color;
        yield return null; // 等待下一帧
    }
    
    color.a = 0;
    renderer.material.color = color;
}

// 启动协程
StartCoroutine(DashCoroutine(2f));
StartCoroutine(FadeOut(myRenderer, 1f));

// 停止协程
StopCoroutine("DashCoroutine");
StopAllCoroutines();
```

### 五、委托与事件

```csharp
// C# 事件系统
public class EventManager : MonoBehaviour
{
    public static EventManager Instance;
    
    // 事件定义
    public event System.Action<int> OnHealthChanged;
    public event System.Action OnPlayerDeath;
    public event System.Action<string> OnGameOver;
    
    void Awake() => Instance = this;
    
    public void HealthChanged(int newHealth) => OnHealthChanged?.Invoke(newHealth);
    public void PlayerDeath() => OnPlayerDeath?.Invoke();
}

// 订阅事件
public class UIManager : MonoBehaviour
{
    void OnEnable()
    {
        EventManager.Instance.OnHealthChanged += UpdateHealthBar;
        EventManager.Instance.OnPlayerDeath += ShowGameOver;
    }
    
    void OnDisable()
    {
        EventManager.Instance.OnHealthChanged -= UpdateHealthBar;
        EventManager.Instance.OnPlayerDeath -= ShowGameOver;
    }
    
    void UpdateHealthBar(int health) { /* 更新UI */ }
    void ShowGameOver() { /* 显示游戏结束 */ }
}

// UnityAction 与 UnityEvent
public UnityEvent OnClick;  // 在 Inspector 中绑定
public UnityEvent<int> OnScoreChanged;
```
