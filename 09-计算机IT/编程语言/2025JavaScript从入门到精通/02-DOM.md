# DOM

## DOM节点与树结构
- DOM（Document Object Model）：将HTML文档表示为树形节点结构
- 节点类型：元素节点（Element）、文本节点（Text）、属性节点（Attr）、注释节点（Comment）
- document节点：DOM树的根节点，代表整个HTML文档
- 节点关系：parentNode、childNodes、firstChild、lastChild、nextSibling、previousSibling
- children只返回元素子节点，childNodes返回所有节点（含文本节点）

## 获取元素
- getElementById()：通过ID获取单个元素
- getElementsByClassName()：通过类名获取HTMLCollection（动态集合）
- getElementsByTagName()：通过标签名获取HTMLCollection
- getElementsByName()：通过name属性获取NodeList
- querySelector()：CSS选择器，返回第一个匹配元素
- querySelectorAll()：CSS选择器，返回所有匹配的NodeList（静态集合）
- 推荐优先使用querySelector/querySelectorAll，语法更灵活

## DOM操作
- 创建元素：document.createElement('tag')
- 添加节点：appendChild()末尾追加、insertBefore(new, ref)指定位置、append()、prepend()
- 删除节点：removeChild()、remove()
- 替换节点：replaceChild(new, old)
- 克隆节点：cloneNode(true)深拷贝含子节点、cloneNode(false)浅拷贝
- 文档片段：document.createDocumentFragment() 批量操作减少重排

## 属性与样式操作
- 获取属性：getAttribute()、element.id、element.className
- 设置属性：setAttribute()、removeAttribute()、hasAttribute()
- dataset：element.dataset.xxx 访问data-xxx自定义属性
- classList：add()、remove()、toggle()、contains() 操作CSS类
- style：element.style.color = 'red' 直接操作内联样式
- getComputedStyle()：获取元素最终计算后的样式

## 事件处理
- 事件监听：addEventListener('click', handler, options) 推荐方式
- 事件移除：removeEventListener() 需传入同一函数引用
- 事件对象：event.target（触发元素）、event.currentTarget（绑定元素）
- 事件冒泡：事件从子元素向父元素传播，e.stopPropagation()阻止
- 事件捕获：addEventListener第三个参数设为true在捕获阶段触发
- 事件委托：在父元素上监听事件，通过event.target判断实际触发元素
- 常用事件：click、dblclick、mouseenter/mouseleave、keydown/keyup、input、submit、scroll、resize
