# BOM

## window对象
- window是浏览器的全局对象，全局变量和函数都是window的属性
- window.innerWidth/innerHeight：视口宽高
- window.outerWidth/outerHeight：浏览器窗口宽高
- window.scrollY/pageYOffset：页面垂直滚动距离
- window.open()：打开新窗口，window.close()关闭
- window.alert()、confirm()、prompt()：对话框（阻塞页面）

## 定时器
- setTimeout(fn, delay)：延迟执行一次，返回定时器ID
- clearTimeout(id)：取消setTimeout
- setInterval(fn, delay)：每隔delay毫秒重复执行
- clearInterval(id)：取消setInterval
- requestAnimationFrame(callback)：下一帧执行，适合动画，浏览器自动优化
- cancelAnimationFrame(id)：取消requestAnimationFrame
- 注意：setInterval有累积延迟问题，递归setTimeout更可靠

## location对象
- location.href：完整URL，设置可跳转页面
- location.protocol/host/hostname/port/pathname/search/hash：URL各部分
- location.assign()：加载新页面（可后退）、location.replace()：替换当前页面（不可后退）
- location.reload()：刷新页面，location.reload(true)强制刷新
- search：查询字符串（?key=value），需手动解析或使用URLSearchParams

## history对象
- history.back()：后退一步、history.forward()：前进一步
- history.go(n)：前进/后退n步，go(0)刷新当前页
- history.pushState(state, title, url)：添加历史记录（不刷新页面）
- history.replaceState(state, title, url)：替换当前历史记录
- popstate事件：浏览器前进/后退时触发
- 单页应用（SPA）路由基于pushState和popstate实现

## navigator与storage
- navigator.userAgent：浏览器用户代理字符串
- navigator.language：浏览器语言、navigator.onLine：是否在线
- navigator.geolocation.getCurrentPosition()：获取地理位置
- localStorage：持久存储（除非手动清除），同源限制，约5-10MB
- sessionStorage：会话级存储（标签页关闭即清除），同源同标签页
- 方法：setItem(key, value)、getItem(key)、removeItem(key)、clear()
- 存储事件：window.addEventListener('storage', callback) 跨标签页同步

## XMLHttpRequest与Fetch
- XMLHttpRequest（XHR）：传统AJAX方式
- XHR流程：new XMLHttpRequest() → open(method, url) → send() → onreadystatechange
- Fetch API（现代）：`fetch(url).then(res => res.json()).then(data => {})`
- fetch选项：method、headers、body、mode、credentials
- fetch不自动reject HTTP错误状态码，需手动检查response.ok
- AbortController：取消fetch请求，`controller.abort()`
