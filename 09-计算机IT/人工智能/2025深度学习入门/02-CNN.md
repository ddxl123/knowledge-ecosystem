# 卷积神经网络（CNN）


## 收集指南

> ⚠️ **严格范围限定：** 仅收集本章（第2章 CNN）相关内容，禁止跨章节引用。

### 条目描述
本文件是《2025深度学习入门》中关于「CNN」的知识原子文件，属于人工智能方向。

### 知识结构
- 卷积操作
- 池化层
- 经典架构
- 迁移学习
- 应用场景

### 待收集原子知识点
- 卷积核与特征提取
- 最大池化/平均池化
- LeNet/AlexNet/ResNet
- 预训练模型微调
- 图像分类/目标检测

## 核心知识点

### 一、卷积操作

```python
import torch
import torch.nn as nn

# 2D 卷积层
conv = nn.Conv2d(
    in_channels=3,      # 输入通道数（RGB=3）
    out_channels=64,    # 输出通道数（卷积核数量）
    kernel_size=3,      # 卷积核大小
    stride=1,           # 步长
    padding=1           # 填充（保持尺寸不变）
)

# 输出尺寸计算
# output_size = (input_size - kernel_size + 2*padding) / stride + 1
# 例：(224 - 3 + 2*1) / 1 + 1 = 224

# 卷积层堆叠
class ConvBlock(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True)
        )
    
    def forward(self, x):
        return self.conv(x)
```

### 二、池化层与下采样

```python
# 最大池化
max_pool = nn.MaxPool2d(kernel_size=2, stride=2)
# 输出尺寸减半：224 → 112

# 平均池化
avg_pool = nn.AvgPool2d(kernel_size=2, stride=2)

# 全局平均池化（GAP）
gap = nn.AdaptiveAvgPool2d(1)  # 输出 (batch, channels, 1, 1)

# 1x1 卷积（通道变换）
conv1x1 = nn.Conv2d(256, 128, 1)  # 改变通道数，不改变空间尺寸
```

### 三、经典 CNN 架构

```python
# 简单 CNN
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            ConvBlock(3, 32),
            nn.MaxPool2d(2),
            ConvBlock(32, 64),
            nn.MaxPool2d(2),
            ConvBlock(64, 128),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(128, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

# ResNet 残差块
class ResBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)
    
    def forward(self, x):
        residual = x
        out = torch.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual  # 残差连接
        return torch.relu(out)
```

### 四、迁移学习

```python
import torchvision.models as models

# 加载预训练模型
model = models.resnet50(weights='IMAGENET1K_V2')

# 冻结特征提取层
for param in model.parameters():
    param.requires_grad = False

# 替换分类头
model.fc = nn.Sequential(
    nn.Linear(2048, 256),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(256, num_classes)
)

# 只训练分类头
optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.001)
```

### 五、CNN 应用场景

- **图像分类：** ResNet、EfficientNet
- **目标检测：** YOLO、Faster R-CNN
- **语义分割：** U-Net、DeepLab
- **图像生成：** GAN 中的生成器/判别器
- **风格迁移：** 利用 CNN 特征提取能力
- **人脸识别：** FaceNet、ArcFace
