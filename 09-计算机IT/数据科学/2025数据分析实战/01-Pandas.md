# Pandas数据处理

## 核心知识点

### 一、DataFrame基础

```python
import pandas as pd
import numpy as np

# 创建DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['Beijing', 'Shanghai', 'Shenzhen']
})

# 读取数据
df = pd.read_csv('data.csv')
df = pd.read_excel('data.xlsx')
df = pd.read_sql('SELECT * FROM users', connection)
df = pd.read_json('data.json')

# 基本信息
df.head()
df.tail()
df.info()
df.describe()
df.shape
df.columns
df.dtypes
```

### 二、数据选择

```python
# 列选择
df['name']
df[['name', 'age']]

# 行选择
df[0:3]

# loc - 标签选择
df.loc[0, 'name']
df.loc[0:2, ['name', 'age']]
df.loc[df['age'] > 25]

# iloc - 位置选择
df.iloc[0, 0]
df.iloc[0:2, 0:2]

# 条件筛选
df[df['age'] > 25]
df[(df['age'] > 25) & (df['city'] == 'Beijing')]
df.query('age > 25 and city == "Beijing"')
```

### 三、数据清洗

```python
# 处理缺失值
df.isnull().sum()
df.dropna()
df.dropna(subset=['name', 'age'])
df.fillna(0)
df.fillna(df.mean())
df['age'].fillna(df['age'].median(), inplace=True)

# 处理重复值
df.duplicated().sum()
df.drop_duplicates()
df.drop_duplicates(subset=['name'], keep='first')

# 数据类型转换
df['date'] = pd.to_datetime(df['date'])
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['category'] = df['category'].astype('category')

# 字符串处理
df['name'].str.lower()
df['name'].str.strip()
df['name'].str.contains('alice')
df['email'].str.extract(r'@(.+)')
```

### 四、数据转换

```python
# 新增列
df['birth_year'] = 2025 - df['age']
df['full_info'] = df['name'] + ' - ' + df['city']

# apply函数
df['age_group'] = df['age'].apply(lambda x: 'young' if x < 30 else 'senior')

# map与replace
df['city_code'] = df['city'].map({'Beijing': 1, 'Shanghai': 2, 'Shenzhen': 3})
df['status'] = df['status'].replace({0: 'inactive', 1: 'active'})

# 排序
df.sort_values('age', ascending=False)
df.sort_values(['city', 'age'], ascending=[True, False])
```

### 五、聚合分析

```python
# groupby
df.groupby('city')['age'].mean()
df.groupby('city').agg({
    'age': ['mean', 'max', 'min'],
    'name': 'count'
})

# 数据透视表
pd.pivot_table(df, values='salary', index='department', columns='gender', aggfunc='mean')

# 交叉表
pd.crosstab(df['city'], df['gender'])

# 滚动计算
df['moving_avg'] = df['sales'].rolling(window=7).mean()
df['cumsum'] = df['sales'].cumsum()
```

### 六、合并与连接

```python
# concat
pd.concat([df1, df2])
pd.concat([df1, df2], axis=1)

# merge
pd.merge(df1, df2, on='id')
pd.merge(df1, df2, left_on='user_id', right_on='id', how='left')

# join
df1.set_index('id').join(df2.set_index('user_id'))
```
