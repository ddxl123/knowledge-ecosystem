# Matplotlib

## 知识点

### 1. 基本绑图
- **导入**: `import matplotlib.pyplot as plt`
- **折线图**: `plt.plot(x, y)`
- **柱状图**: `plt.bar(x, y)`
- **散点图**: `plt.scatter(x, y)`
- **显示**: `plt.show()`

### 2. 图表元素
- **标题**: `plt.title('图表标题')`
- **坐标轴标签**: `plt.xlabel('X轴')`、`plt.ylabel('Y轴')`
- **图例**: `plt.legend(['系列1','系列2'])`
- **网格**: `plt.grid(True)`
- **要点**: 每个图表都应有标题和坐标轴标签

### 3. 子图布局
- **方法一**: `fig, axes = plt.subplots(2, 2)` 创建2×2子图
- **方法二**: `plt.subplot(2, 2, 1)` 选择子图位置
- **调整间距**: `plt.tight_layout()` 自动调整子图间距
- **共享坐标轴**: `subplots(sharex=True, sharey=True)`

### 4. 样式定制
- **颜色**: color='red'、color='#FF5733'、color='C0'（默认色序）
- **线型**: linestyle='--'(虚线)、':'(点线)、'-.'(点划线)
- **标记**: marker='o'(圆形)、's'(方形)、'^'(三角)
- **预设风格**: `plt.style.use('seaborn')` 使用预设主题

### 5. 高级图表
- **直方图**: `plt.hist(data, bins=30)` 查看数据分布
- **箱线图**: `plt.boxplot(data)` 查看数据分布和异常值
- **热力图**: `plt.imshow(matrix, cmap='coolwarm')`
- **饼图**: `plt.pie(sizes, labels=labels)`

### 6. 保存与输出
- **保存图片**: `plt.savefig('figure.png', dpi=300, bbox_inches='tight')`
- **格式**: PNG、PDF、SVG、EPS 等
- **分辨率**: dpi参数控制分辨率，论文用300dpi以上
- **要点**: 保存要在plt.show()之前，否则保存空白图
