# Hook

## useState与useEffect
- useState：`const [state, setState] = useState(initialValue)` 声明状态
- 惰性初始化：`useState(() => expensiveCompute())` 只在首次渲染执行
- useEffect：`useEffect(() => { 副作用代码 }, [依赖数组])` 处理副作用
- 依赖数组：`[]`空数组只执行一次、不传每次渲染执行、`[dep]`依赖变化时执行
- 清理函数：`useEffect(() => { const sub = subscribe(); return () => sub.unsubscribe(); })`
- 常见副作用：数据获取、订阅、DOM操作、定时器
- 执行时机：每次渲染后、DOM更新后、浏览器绘制后

## useContext与useReducer
- useContext：`const value = useContext(MyContext)` 消费Context值
- Context创建：`const MyContext = React.createContext(defaultValue)`
- Provider：`<MyContext.Provider value={data}>{children}</MyContext.Provider>`
- useReducer：复杂状态逻辑，`const [state, dispatch] = useReducer(reducer, initialState)`
- reducer函数：`function reducer(state, action) { switch(action.type) { ... } }`
- dispatch：`dispatch({ type: 'INCREMENT', payload: 1 })` 触发状态更新
- useState vs useReducer：简单状态用useState，复杂逻辑/多子值用useReducer

## useMemo与useCallback
- useMemo：`const memoized = useMemo(() => computeExpensive(a, b), [a, b])` 缓存计算结果
- useCallback：`const memoizedFn = useCallback(() => doSomething(a), [a])` 缓存函数引用
- 使用场景：避免子组件不必要的重渲染（配合React.memo）
- React.memo：`const MemoChild = React.memo(Child)` props不变时跳过重渲染
- 不要过度优化：只有性能确实有问题时才使用memo/useMemo/useCallback
- 依赖准确性：依赖数组必须包含所有用到的外部变量

## useRef与自定义Hook
- useRef：`const ref = useRef(initialValue)` 创建可变引用，不触发重渲染
- DOM引用：`<input ref={inputRef} />` → `inputRef.current.focus()`
- 保存前值：`prevValue = useRef(value)` 在effect中更新
- 自定义Hook：以use开头的函数，封装可复用的状态逻辑
- 示例：`function useLocalStorage(key, initialValue) { const [value, setValue] = useState(() => localStorage.getItem(key) ?? initialValue); ... }`
- 规则：只能在函数组件或自定义Hook中调用Hook，不能在条件/循环中调用

## 高级Hook与模式
- useId（React 18）：生成唯一ID，用于无障碍属性
- useTransition（React 18）：`const [isPending, startTransition] = useTransition()` 低优先级更新
- useDeferredValue（React 18）：`const deferred = useDeferredValue(value)` 延迟更新
- useSyncExternalStore（React 18）：订阅外部数据源
- useImperativeHandle：配合forwardRef暴露子组件方法给父组件
- forwardRef：`React.forwardRef((props, ref) => <input ref={ref} />)` 转发ref
- 错误边界：类组件实现componentDidCatch，函数组件用react-error-boundary库
