# C#编程基础

## 核心知识点

### 一、Unity中的C#

```csharp
using UnityEngine;

public class MyFirstScript : MonoBehaviour
{
    // 公开属性（可在Inspector中编辑）
    public int health = 100;
    public float speed = 5.0f;
    public string playerName = "Player";
    public GameObject bulletPrefab;

    // 私有属性
    private Rigidbody rb;
    private bool isAlive = true;

    // 生命周期方法
    void Awake()
    {
        // 最早调用，用于初始化引用
        rb = GetComponent<Rigidbody>();
    }

    void Start()
    {
        // 第一帧前调用
        Debug.Log($"{playerName} initialized!");
    }

    void Update()
    {
        // 每帧调用
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        transform.Translate(new Vector3(horizontal, 0, vertical) * speed * Time.deltaTime);
    }

    void FixedUpdate()
    {
        // 固定时间间隔调用（用于物理）
        rb.AddForce(Vector3.forward * 10f);
    }

    void OnDestroy()
    {
        // 对象销毁时调用
    }
}
```

### 二、协程

```csharp
public class CoroutineExample : MonoBehaviour
{
    void Start()
    {
        StartCoroutine(Countdown(5));
        StartCoroutine(SpawnEnemies());
    }

    IEnumerator Countdown(int seconds)
    {
        for (int i = seconds; i > 0; i--)
        {
            Debug.Log($"Countdown: {i}");
            yield return new WaitForSeconds(1);
        }
        Debug.Log("Go!");
    }

    IEnumerator SpawnEnemies()
    {
        while (true)
        {
            Instantiate(enemyPrefab, spawnPoint.position, Quaternion.identity);
            yield return new WaitForSeconds(Random.Range(1f, 3f));
        }
    }

    // 停止协程
    void StopSpawning()
    {
        StopCoroutine("SpawnEnemies");
        StopAllCoroutines();
    }
}
```

### 三、单例模式

```csharp
public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    public int score = 0;
    public bool isGameOver = false;

    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    public void AddScore(int points)
    {
        score += points;
        Debug.Log($"Score: {score}");
    }

    public void GameOver()
    {
        isGameOver = true;
        Time.timeScale = 0;
    }
}
```

### 四、事件系统

```csharp
using System;

public class EventManager : MonoBehaviour
{
    public static event Action<int> OnScoreChanged;
    public static event Action OnGameOver;
    public static event Action<string> OnPlayerDied;

    public static void ScoreChanged(int score)
    {
        OnScoreChanged?.Invoke(score);
    }

    public static void GameOver()
    {
        OnGameOver?.Invoke();
    }
}

// 订阅事件
public class UIManager : MonoBehaviour
{
    void OnEnable()
    {
        EventManager.OnScoreChanged += UpdateScoreUI;
        EventManager.OnGameOver += ShowGameOverScreen;
    }

    void OnDisable()
    {
        EventManager.OnScoreChanged -= UpdateScoreUI;
        EventManager.OnGameOver -= ShowGameOverScreen;
    }

    void UpdateScoreUI(int score)
    {
        scoreText.text = $"Score: {score}";
    }
}
```

### 五、ScriptableObject

```csharp
[CreateAssetMenu(fileName = "NewWeapon", menuName = "Game/Weapon")]
public class WeaponData : ScriptableObject
{
    public string weaponName;
    public int damage;
    public float fireRate;
    public float range;
    public GameObject bulletPrefab;
    public Sprite icon;
}

// 使用
public class Weapon : MonoBehaviour
{
    public WeaponData weaponData;

    void Fire()
    {
        Instantiate(weaponData.bulletPrefab, firePoint.position, firePoint.rotation);
    }
}
```
