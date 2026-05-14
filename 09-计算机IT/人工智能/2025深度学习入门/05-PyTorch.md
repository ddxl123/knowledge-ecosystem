# PyTorch 实战


## 收集指南

> ⚠️ **严格范围限定：** 仅收集本章（第5章 PyTorch）相关内容，禁止跨章节引用。

### 条目描述
本文件是《2025深度学习入门》中关于「PyTorch」的知识原子文件，属于人工智能方向。

### 知识结构
- 张量操作
- 数据加载
- 模型训练流程
- GPU 加速
- 模型部署

### 待收集原子知识点
- Tensor 基础操作
- Dataset/DataLoader
- 训练循环与验证
- CUDA 与混合精度
- TorchScript/ONNX 导出

## 核心知识点

### 一、张量操作

```python
import torch

# 创建张量
x = torch.tensor([1, 2, 3])
x = torch.zeros(3, 4)
x = torch.randn(3, 4)          # 正态分布随机
x = torch.arange(0, 10, 2)     # [0, 2, 4, 6, 8]

# 基础操作
x.shape                 # 形状
x.reshape(2, 3)         # 变形
x.unsqueeze(0)          # 增加维度
x.squeeze()             # 去除维度
x.view(2, 3)            # 变形（连续内存）
x.item()                # 标量转 Python 数值

# 数学运算
a + b                   # 逐元素加
a * b                   # 逐元素乘
a @ b                   # 矩阵乘法
torch.matmul(a, b)      # 矩阵乘法
a.mean() / a.sum()      # 聚合

# 自动求导
x = torch.tensor(2.0, requires_grad=True)
y = x ** 2 + 3 * x
y.backward()
print(x.grad)           # dy/dx = 2x + 3 = 7
```

### 二、数据加载

```python
from torch.utils.data import Dataset, DataLoader

class MyDataset(Dataset):
    def __init__(self, data, labels, transform=None):
        self.data = data
        self.labels = labels
        self.transform = transform
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        sample = self.data[idx]
        label = self.labels[idx]
        if self.transform:
            sample = self.transform(sample)
        return sample, label

# DataLoader
train_dataset = MyDataset(train_data, train_labels)
train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4,
    pin_memory=True,
    drop_last=True
)

# 图像数据预处理
from torchvision import transforms
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])
```

### 三、模型训练流程

```python
# 完整训练循环
def train(model, train_loader, val_loader, epochs=10):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    
    for epoch in range(epochs):
        # 训练阶段
        model.train()
        train_loss = 0
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            
            optimizer.zero_grad()
            output = model(batch_x)
            loss = criterion(output, batch_y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            train_loss += loss.item()
        
        # 验证阶段
        model.eval()
        val_loss, correct = 0, 0
        with torch.no_grad():
            for batch_x, batch_y in val_loader:
                batch_x, batch_y = batch_x.to(device), batch_y.to(device)
                output = model(batch_x)
                val_loss += criterion(output, batch_y).item()
                correct += (output.argmax(1) == batch_y).sum().item()
        
        scheduler.step()
        print(f'Epoch {epoch+1}: Train Loss={train_loss/len(train_loader):.4f}, '
              f'Val Acc={correct/len(val_loader.dataset):.4f}')
```

### 四、GPU 加速与混合精度

```python
# CUDA 操作
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
data = data.to(device)

# 混合精度训练（节省显存、加速训练）
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
for batch_x, batch_y in train_loader:
    optimizer.zero_grad()
    with autocast():
        output = model(batch_x.to(device))
        loss = criterion(output, batch_y.to(device))
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()

# 多 GPU 训练
model = nn.DataParallel(model)  # 数据并行
# 或使用 DistributedDataParallel（推荐）
model = nn.parallel.DistributedDataParallel(model)
```

### 五、模型导出与部署

```python
# TorchScript 导出
scripted_model = torch.jit.script(model)
scripted_model.save('model.pt')

# ONNX 导出
dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(model, dummy_input, 'model.onnx',
                  input_names=['input'], output_names=['output'],
                  dynamic_axes={'input': {0: 'batch_size'}})

# 模型保存与加载
torch.save(model.state_dict(), 'model.pth')
model.load_state_dict(torch.load('model.pth'))
```
