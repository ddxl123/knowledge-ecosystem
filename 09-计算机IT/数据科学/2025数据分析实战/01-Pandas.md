# Pandas 数据处理


## 收集指南

> ⚠️ **严格范围限定：** 仅收集本章（第1章 Pandas）相关内容，禁止跨章节引用。

### 条目描述
本文件是《2025数据分析实战》中关于「Pandas」的知识原子文件，属于数据科学方向。

### 知识结构
- DataFrame 与 Series
- 数据读写
- 数据清洗
- 数据转换
- 数据聚合

### 待收集原子知识点
- Pandas 核心数据结构
- CSV/Excel/SQL 读写
- 缺失值与异常值处理
- apply/map/transform
- groupby 与 pivot_table

## 核心知识点

### 一、DataFrame 与 Series

```python
import pandas as pd
import numpy as np

# Series（一维带标签数组）
s = pd.Series([1, 3, 5, 7], index=['a', 'b', 'c', 'd'], name='numbers')

# DataFrame（二维表格）
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['Beijing', 'Shanghai', 'Shenzhen']
})

# 基础操作
df.shape           # (3, 3)
df.dtypes          # 列类型
df.info()          # 详细信息
df.describe()      # 统计摘要
df.head(5)         # 前5行
df.columns         # 列名
df.index           # 索引

# 选择数据
df['name']                     # 选择单列
df[['name', 'age']]           # 选择多列
df.loc[0]                      # 按标签选择行
df.loc[0:2, 'name':'age']     # 标签切片
df.iloc[0:2, 0:2]             # 位置切片
df[df['age'] > 25]            # 条件筛选
df.query('age > 25 and city == "Beijing"')  # 查询语法
```

### 二、数据读写

```python
# CSV
df = pd.read_csv('data.csv', encoding='utf-8', sep=',')
df.to_csv('output.csv', index=False, encoding='utf-8-sig')

# Excel
df = pd.read_excel('data.xlsx', sheet_name='Sheet1', header=0)
df.to_excel('output.xlsx', sheet_name='结果', index=False)

# JSON
df = pd.read_json('data.json', orient='records')
df.to_json('output.json', orient='records', force_ascii=False)

# SQL
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://user:pass@localhost:3306/mydb')
df = pd.read_sql('SELECT * FROM users', engine)
df.to_sql('users', engine, if_exists='append', index=False)

# 大文件分块读取
chunks = pd.read_csv('big.csv', chunksize=10000)
for chunk in chunks:
    process(chunk)
```

### 三、数据清洗

```python
# 缺失值处理
df.isnull().sum()               # 统计缺失值
df.dropna()                     # 删除含缺失值的行
df.dropna(subset=['name'])     # 只检查特定列
df.fillna(0)                    # 用0填充
df.fillna(df.mean())            # 用均值填充
df.fillna(method='ffill')      # 前向填充
df['age'].interpolate()        # 插值填充

# 重复值处理
df.duplicated().sum()           # 统计重复行
df.drop_duplicates()            # 删除重复行
df.drop_duplicates(subset=['name'], keep='first')

# 数据类型转换
df['age'] = df['age'].astype(int)
df['date'] = pd.to_datetime(df['date'])
df['category'] = df['category'].astype('category')

# 字符串处理
df['name'] = df['name'].str.strip()
df['email'] = df['email'].str.lower()
df['phone'] = df['phone'].str.replace('-', '')
df['city_code'] = df['city'].str[:2]

# 异常值处理
Q1 = df['salary'].quantile(0.25)
Q3 = df['salary'].quantile(0.75)
IQR = Q3 - Q1
df_clean = df[(df['salary'] >= Q1 - 1.5*IQR) & (df['salary'] <= Q3 + 1.5*IQR)]
```

### 四、数据转换

```python
# apply：对行或列应用函数
df['age_group'] = df['age'].apply(lambda x: '青年' if x < 35 else '中年')
df['full_info'] = df.apply(lambda row: f"{row['name']}-{row['city']}", axis=1)

# map：映射替换
city_map = {'Beijing': '北京', 'Shanghai': '上海'}
df['city_cn'] = df['city'].map(city_map)

# replace：替换值
df['status'] = df['status'].replace({0: 'inactive', 1: 'active'})

# 排序
df.sort_values('age', ascending=False)
df.sort_values(['city', 'age'], ascending=[True, False])

# 重塑
df_wide = df.pivot(index='date', columns='product', values='sales')
df_long = pd.melt(df, id_vars=['date'], value_vars=['A', 'B'], var_name='product', value_name='sales')

# 合并
merged = pd.merge(df1, df2, on='user_id', how='left')
concatenated = pd.concat([df1, df2], axis=0, ignore_index=True)
```

### 五、数据聚合

```python
# groupby 分组聚合
df.groupby('city')['salary'].mean()
df.groupby('city').agg({'salary': ['mean', 'max', 'min'], 'age': 'median'})
df.groupby(['city', 'department']).agg(
    avg_salary=('salary', 'mean'),
    count=('name', 'count')
).reset_index()

# pivot_table 透视表
pd.pivot_table(df, values='salary', index='city', columns='department',
               aggfunc='mean', fill_value=0)

# 时间序列重采样
df.set_index('date').resample('M')['sales'].sum()  # 按月汇总
df.set_index('date').resample('Q')['sales'].mean()  # 按季度均值

# 滚动计算
df['ma7'] = df['sales'].rolling(window=7).mean()   # 7日移动平均
df['cumsum'] = df['sales'].cumsum()                  # 累计求和
```
