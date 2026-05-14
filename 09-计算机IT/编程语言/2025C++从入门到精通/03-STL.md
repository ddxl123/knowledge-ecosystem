# STL

## 容器概述
- STL容器分类：顺序容器、关联容器、无序容器、容器适配器
- 顺序容器：vector、deque、list、forward_list、array
- 关联容器：set、map、multiset、multimap（基于红黑树，有序）
- 无序容器：unordered_set、unordered_map、unordered_multiset、unordered_multimap（基于哈希表）
- 容器适配器：stack、queue、priority_queue

## 顺序容器
- vector：动态数组，连续内存，随机访问O(1)，尾部插入O(1)均摊，中间插入O(n)
- deque：双端队列，分段连续内存，首尾插入O(1)，随机访问O(1)
- list：双向链表，任意位置插入删除O(1)，不支持随机访问
- forward_list：单向链表，更节省内存，C++11新增
- array：固定大小数组，栈上分配，比原生数组更安全
- 常用操作：push_back、pop_back、insert、erase、size、empty、clear、begin/end

## 关联容器
- set：不重复元素集合，自动排序，查找O(log n)
- map：键值对映射，key不重复，自动按key排序
- multiset/multimap：允许重复key
- 插入：insert()、emplace()（原地构造，C++11）
- 查找：find()返回迭代器、count()计数、lower_bound/upper_bound
- []运算符：map特有，不存在时自动插入默认值
- at()方法：不存在时抛出out_of_range异常
- 结构化绑定遍历（C++17）：`for(auto& [key, value] : myMap) {}`

## 无序容器
- unordered_set/unordered_map：基于哈希表，平均O(1)查找
- 桶（bucket）结构：哈希冲突用链表或开放寻址解决
- 负载因子：元素数/桶数，超过阈值自动rehash
- 自定义哈希：重载hash函数对象或提供自定义哈希函数
- 适用场景：不需要排序、需要快速查找的场景

## 迭代器
- 迭代器类型：输入、输出、前向、双向、随机访问
- begin()/end()：返回首元素和尾后迭代器
- rbegin()/rend()：反向迭代器
- 迭代器失效：vector插入/删除后、map删除后其他迭代器不失效
- auto关键字简化：`auto it = vec.begin();`
- 范围for本质：使用begin/end迭代器遍历

## 算法
- `<algorithm>` 头文件包含大量通用算法
- 非修改算法：find、count、for_each、search、equal、mismatch
- 修改算法：copy、transform、replace、fill、generate、remove、unique
- 排序算法：sort、stable_sort、partial_sort、nth_element
- 二分查找：binary_search、lower_bound、upper_bound、equal_range
- 集合算法：set_union、set_intersection、set_difference
- 堆操作：make_heap、push_heap、pop_heap、sort_heap
- Lambda作为算法参数：`sort(v.begin(), v.end(), [](int a, int b){ return a > b; })`
