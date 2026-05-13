# DOM操作

## 核心知识点

### 一、DOM基础

#### 1. 什么是DOM
- DOM（Document Object Model）文档对象模型
- 将HTML文档表示为树形结构
- 通过JavaScript操作HTML元素

### 二、节点查询

#### 1. 常用查询方法
```javascript
// 通过ID查询
const el = document.getElementById("app");

// 通过类名查询
const items = document.getElementsByClassName("item");

// 通过标签名查询
const divs = document.getElementsByTagName("div");

// CSS选择器（推荐）
const el = document.querySelector(".container > .title");
const els = document.querySelectorAll(".item");
```

#### 2. 节点关系
```javascript
el.parentNode;      // 父节点
el.children;        // 子元素集合
el.firstElementChild; // 第一个子元素
el.lastElementChild;  // 最后一个子元素
el.nextElementSibling; // 下一个兄弟元素
el.previousElementSibling; // 上一个兄弟元素
```

### 三、节点操作

#### 1. 创建与插入
```javascript
// 创建元素
const div = document.createElement("div");
div.textContent = "Hello";

// 插入节点
parent.appendChild(child);           // 追加到末尾
parent.insertBefore(new, ref);       // 插入到ref之前
parent.append(child1, child2);       // 追加多个
parent.prepend(child);               // 插入到开头

// 替换与删除
parent.replaceChild(newChild, oldChild);
parent.removeChild(child);
child.remove(); // 现代方法
```

#### 2. 克隆节点
```javascript
const clone = el.cloneNode(true); // 深克隆
const clone = el.cloneNode(false); // 浅克隆
```

### 四、属性操作
```javascript
// HTML属性
el.getAttribute("class");
el.setAttribute("id", "main");
el.removeAttribute("disabled");
el.hasAttribute("data-id");

// data属性
el.dataset.userId; // data-user-id

// 类名操作
el.classList.add("active");
el.classList.remove("active");
el.classList.toggle("active");
el.classList.contains("active"); // true/false

// 内容操作
el.innerHTML = "<b>Bold</b>"; // HTML内容
el.textContent = "Text";      // 文本内容
el.innerText = "Visible";     // 可见文本
```

### 五、样式操作
```javascript
// 内联样式
el.style.color = "red";
el.style.backgroundColor = "#f0f0f0";
el.style.display = "none";

// 获取计算样式
const style = window.getComputedStyle(el);
console.log(style.width);
```

### 六、事件处理

#### 1. 事件监听
```javascript
// addEventListener（推荐）
el.addEventListener("click", function(e) {
    e.preventDefault(); // 阻止默认行为
    e.stopPropagation(); // 阻止冒泡
    console.log(e.target); // 触发事件的元素
}, { once: true }); // 只触发一次

// 移除监听
el.removeEventListener("click", handler);
```

#### 2. 事件委托
```javascript
// 利用事件冒泡，在父元素上监听
document.querySelector(".list").addEventListener("click", (e) => {
    if (e.target.matches(".item")) {
        console.log("Clicked:", e.target.textContent);
    }
});
```

#### 3. 常用事件类型
| 类型 | 事件 |
|------|------|
| 鼠标 | click, dblclick, mouseenter, mouseleave, mousemove |
| 键盘 | keydown, keyup, keypress |
| 表单 | submit, change, input, focus, blur |
| 窗口 | load, resize, scroll, unload |
| 触摸 | touchstart, touchmove, touchend |
