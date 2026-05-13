# Pandas

## 知识点

### 1. Series与DataFrame
- **Series**: 一维带标签数组，类似字典 `pd.Series([1,2,3], index=['a','b','c'])`
- **DataFrame**: 二维表格结构，由多个Series组成
- **创建**: `pd.DataFrame({'列名1': data1, '列名2': data2})`
- **读取数据**: `pd.read_csv()`、`pd.read_excel()`、`pd.read_sql()`

### 2. 数据选择与过滤
- **列选择**: `df['列名']` 或 `df[['列1','列2']]`
- **行选择**: `df.loc[标签]` 或 `df.iloc[位置]`
- **条件过滤**: `df[df['age'] > 30]`
- **链式操作**: `df.loc[df['city']=='北京', ['name','age']]`

### 3. 数据处理
- **缺失值**: `df.isnull()` 检测、`df.fillna(0)` 填充、`df.dropna()` 删除
- **去重**: `df.drop_duplicates()`
- **排序**: `df.sort_values('列名', ascending=False)`
- **类型转换**: `df['列名'].astype(int)`

### 4. 分组与聚合
- **groupby**: `df.groupby('类别')['数值'].mean()`
- **多列分组**: `df.groupby(['省','市'])['销量'].sum()`
- **多聚合函数**: `df.groupby('类别').agg({'销量':'sum', '价格':'mean'})`
- **透视表**: `pd.pivot_table(df, values='销量', index='省', columns='年份')`

### 5. 合并与连接
- **concat**: `pd.concat([df1, df2])` 纵向或横向拼接
- **merge**: `pd.merge(df1, df2, on='key')` 类似SQL的JOIN
- **join**: `df1.join(df2)` 按索引连接
- **参数**: how='left'/'right'/'inner'/'outer' 控制连接方式

### 6. 时间序列
- **日期索引**: `pd.to_datetime()` 转换为日期类型
- **重采样**: `df.resample('M').sum()` 按月汇总
- **滚动计算**: `df['销量'].rolling(7).mean()` 7天移动平均
- **时间差**: `pd.Timedelta` 计算时间间隔

## 收集指南

> ⚠️ **严格范围限定：** 仅收集本文件内容，禁止跨文件、跨目录引用。例如本文件为「Pandas」，则只收集该主题内容，不得涉及其他主题

### 概述

**Pandas** 是职业技能领域的核心知识模块，涉及专业知识、实操技能和职业素养。

### 知识结构

本部分内容按以下结构组织：


### 学习要点

- 理解核心概念的定义和内涵
- 掌握知识之间的逻辑关系
- 通过练习和应用巩固理解
