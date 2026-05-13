# STL标准模板库

## 核心知识点

### 一、STL概述
STL（Standard Template Library）包含六大组件：
- **容器（Container）** — 数据结构
- **迭代器（Iterator）** — 访问容器元素的接口
- **算法（Algorithm）** — 操作容器的函数
- **仿函数（Functor）** — 函数对象
- **适配器（Adapter）** — 修改接口
- **分配器（Allocator）** — 内存管理

### 二、序列容器

#### 1. vector
```cpp
vector<int> v = {1, 2, 3};
v.push_back(4);       // 尾部添加
v.pop_back();         // 删除尾部
v[0];                 // 随机访问
v.size();             // 元素个数
```

#### 2. deque
```cpp
deque<int> dq;
dq.push_front(1);  // 头部添加
dq.push_back(2);   // 尾部添加
```

#### 3. list
```cpp
list<int> lst = {1, 2, 3};
lst.push_front(0);
lst.push_back(4);
lst.sort();  // 链表排序
```

### 三、关联容器

#### 1. set / multiset
```cpp
set<int> s = {3, 1, 4, 1, 5}; // 自动排序，去重
// s: {1, 3, 4, 5}
s.insert(2);
s.count(3); // 1（存在）或 0（不存在）
```

#### 2. map / multimap
```cpp
map<string, int> mp;
mp["alice"] = 90;
mp["bob"] = 85;
for (auto& [k, v] : mp) {  // C++17结构化绑定
    cout << k << ": " << v << endl;
}
```

### 四、容器适配器
```cpp
stack<int> stk;    // 栈（LIFO）
queue<int> que;    // 队列（FIFO）
priority_queue<int> pq; // 优先队列（最大堆）
```

### 五、常用算法
```cpp
#include <algorithm>
vector<int> v = {3, 1, 4, 1, 5};

sort(v.begin(), v.end());           // 排序
reverse(v.begin(), v.end());        // 反转
auto it = find(v.begin(), v.end(), 4); // 查找
int cnt = count(v.begin(), v.end(), 1); // 计数
auto it = lower_bound(v.begin(), v.end(), 3); // 二分查找
for_each(v.begin(), v.end(), [](int x){ cout << x; }); // 遍历
```
