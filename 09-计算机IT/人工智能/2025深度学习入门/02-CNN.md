# 卷积神经网络（CNN）

## 核心知识点

### 一、卷积层

#### 1. 卷积操作
```
输入特征图 × 卷积核 = 输出特征图

参数：
- kernel_size：卷积核大小（如3×3）
- stride：步长
- padding：填充
- 输出尺寸 = (输入尺寸 - 卷积核 + 2×填充) / 步长 + 1
```

#### 2. PyTorch实现
```python
import torch.nn as nn

# 2D卷积
conv = nn.Conv2d(
    in_channels=3,      # 输入通道数（RGB=3）
    out_channels=64,    # 输出通道数（滤波器数量）
    kernel_size=3,      # 卷积核大小
    stride=1,           # 步长
    padding=1           # 填充
)

# 输出形状
# 输入: (batch, 3, 224, 224)
# 输出: (batch, 64, 224, 224)
```

#### 3. 1×1卷积
```python
# 通道数变换
conv1x1 = nn.Conv2d(256, 64, kernel_size=1)
# 作用：降维/升维，增加非线性
```

### 二、池化层

#### 1. 最大池化
```python
pool = nn.MaxPool2d(kernel_size=2, stride=2)
# 输入: (batch, 64, 224, 224)
# 输出: (batch, 64, 112, 112)
```

#### 2. 平均池化
```python
pool = nn.AvgPool2d(kernel_size=2, stride=2)
```

#### 3. 全局平均池化
```python
pool = nn.AdaptiveAvgPool2d(1)  # 输出1×1
# 输入: (batch, 512, 7, 7)
# 输出: (batch, 512, 1, 1)
```

### 三、经典CNN架构

#### 1. LeNet-5（1998）
```
输入(32×32) → Conv → Pool → Conv → Pool → FC → FC → 输出
```

#### 2. AlexNet（2012）
```
输入(227×227) → Conv → Pool → Conv → Pool → Conv → Conv → Conv → Pool → FC → FC → FC → 输出
创新：ReLU、Dropout、数据增强
```

#### 3. VGGNet（2014）
```
使用3×3小卷积核堆叠
VGG-16: 13个卷积层 + 3个全连接层
VGG-19: 16个卷积层 + 3个全连接层
```

#### 4. ResNet（2015）
```python
# 残差块
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()
        
        # 残差连接
        self.shortcut = nn.Sequential()
        if in_channels != out_channels:
            self.shortcut = nn.Conv2d(in_channels, out_channels, 1)
    
    def forward(self, x):
        residual = self.shortcut(x)
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual  # 残差连接
        out = self.relu(out)
        return out
```

#### 5. 其他架构
| 架构 | 特点 | 年份 |
|------|------|------|
| GoogLeNet | Inception模块 | 2014 |
| DenseNet | 密集连接 | 2017 |
| EfficientNet | 复合缩放 | 2019 |
| ConvNeXt | 现代化CNN | 2022 |

### 四、迁移学习

#### 1. 预训练模型
```python
import torchvision.models as models

# 加载预训练ResNet
model = models.resnet50(pretrained=True)

# 冻结参数
for param in model.parameters():
    param.requires_grad = False

# 替换最后一层
model.fc = nn.Linear(2048, num_classes)

# 只训练最后一层
optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.001)
```

#### 2. 微调策略
```
- 特征提取：冻结所有层，只训练最后分类层
- 微调：解冻部分层，使用小学习率
- 全部微调：解冻所有层，使用更小学习率
```

### 五、数据增强
```python
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
```

### 六、目标检测基础

#### 1. 常见任务
- 图像分类：识别图片类别
- 目标检测：定位+分类
- 语义分割：像素级分类
- 实例分割：区分不同实例

#### 2. 经典模型
| 模型 | 类型 | 特点 |
|------|------|------|
| R-CNN系列 | 两阶段 | 精度高 |
| YOLO系列 | 单阶段 | 速度快 |
| SSD | 单阶段 | 多尺度 |
| DETR | Transformer | 端到端 |
