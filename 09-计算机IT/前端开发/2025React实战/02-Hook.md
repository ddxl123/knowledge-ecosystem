# Hook深入

## 核心知识点

### 一、useState

```jsx
function Counter() {
    const [count, setCount] = useState(0);

    // 函数式更新
    const increment = () => setCount(prev => prev + 1);

    // 对象状态
    const [user, setUser] = useState({ name: '', age: 0 });
    const updateName = (name) => setUser(prev => ({ ...prev, name }));

    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={increment}>+</button>
        </div>
    );
}
```

### 二、useEffect

```jsx
function UserProfile({ userId }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let cancelled = false;

        async function fetchUser() {
            setLoading(true);
            try {
                const response = await fetch(`/api/users/${userId}`);
                const data = await response.json();
                if (!cancelled) {
                    setUser(data);
                }
            } finally {
                if (!cancelled) {
                    setLoading(false);
                }
            }
        }

        fetchUser();

        return () => {
            cancelled = true; // 清理函数
        };
    }, [userId]); // 依赖数组

    if (loading) return <p>Loading...</p>;
    if (!user) return <p>User not found</p>;

    return <div>{user.name}</div>;
}
```

### 三、useContext

```jsx
const ThemeContext = React.createContext('light');

function ThemeProvider({ children }) {
    const [theme, setTheme] = useState('light');

    const toggleTheme = () => {
        setTheme(prev => prev === 'light' ? 'dark' : 'light');
    };

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
}

function ThemedButton() {
    const { theme, toggleTheme } = useContext(ThemeContext);

    return (
        <button
            className={`btn-${theme}`}
            onClick={toggleTheme}
        >
            Toggle Theme
        </button>
    );
}
```

### 四、useReducer

```jsx
const initialState = { count: 0, step: 1 };

function reducer(state, action) {
    switch (action.type) {
        case 'increment':
            return { ...state, count: state.count + state.step };
        case 'decrement':
            return { ...state, count: state.count - state.step };
        case 'setStep':
            return { ...state, step: action.payload };
        case 'reset':
            return initialState;
        default:
            throw new Error(`Unknown action: ${action.type}`);
    }
}

function Counter() {
    const [state, dispatch] = useReducer(reducer, initialState);

    return (
        <div>
            <p>Count: {state.count}</p>
            <button onClick={() => dispatch({ type: 'increment' })}>+</button>
            <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
            <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
        </div>
    );
}
```

### 五、自定义Hook

```jsx
// useLocalStorage
function useLocalStorage(key, initialValue) {
    const [value, setValue] = useState(() => {
        const stored = localStorage.getItem(key);
        return stored ? JSON.parse(stored) : initialValue;
    });

    useEffect(() => {
        localStorage.setItem(key, JSON.stringify(value));
    }, [key, value]);

    return [value, setValue];
}

// useFetch
function useFetch(url) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let cancelled = false;

        fetch(url)
            .then(res => res.json())
            .then(data => { if (!cancelled) setData(data); })
            .catch(err => { if (!cancelled) setError(err); })
            .finally(() => { if (!cancelled) setLoading(false); });

        return () => { cancelled = true; };
    }, [url]);

    return { data, loading, error };
}

// useDebounce
function useDebounce(value, delay = 300) {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
        const timer = setTimeout(() => setDebouncedValue(value), delay);
        return () => clearTimeout(timer);
    }, [value, delay]);

    return debouncedValue;
}
```

### 六、useMemo与useCallback

```jsx
function ExpensiveComponent({ items, filter }) {
    // useMemo缓存计算结果
    const filteredItems = useMemo(() => {
        return items.filter(item => item.name.includes(filter));
    }, [items, filter]);

    // useCallback缓存函数
    const handleClick = useCallback((id) => {
        console.log('Clicked:', id);
    }, []);

    return (
        <ul>
            {filteredItems.map(item => (
                <Item key={item.id} item={item} onClick={handleClick} />
            ))}
        </ul>
    );
}
```
