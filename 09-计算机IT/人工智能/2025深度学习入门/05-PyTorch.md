# PyTorch实战

## 核心知识点

### 一、张量操作

#### 1. 创建张量
```python
import torch

# 从列表创建
x = torch.tensor([1, 2, 3])
x = torch.tensor([[1, 2], [3, 4]])

# 特殊张量
zeros = torch.zeros(3, 4)
ones = torch.ones(3, 4)
rand = torch.randn(3, 4)  # 正态分布
range = torch.arange(0, 10, 2)

# 从NumPy转换
import numpy as np
np_array = np.array([1, 2, 3])
tensor = torch.from_numpy(np_array)
```

#### 2. 张量操作
```python
x = torch.randn(3, 4)

# 形状操作
x.shape           # torch.Size([3, 4])
x.reshape(4, 3)   # 重塑
x.view(4, 3)      # 重塑（连续内存）
x.unsqueeze(0)    # 增加维度
x.squeeze()       # 去除维度

# 索引与切片
x[0, :]           # 第一行
x[:, 0]           # 第一列
x[1:3, 0:2]       # 切片

# 数学运算
x + y             # 加法
x * y             # 逐元素乘法
torch.mm(x, y)    # 矩阵乘法
x @ y             # 矩阵乘法（简写）
torch.sum(x)      # 求和
torch.mean(x)     # 均值
```

#### 3. GPU加速
```python
# 检查CUDA
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 张量移到GPU
x = x.to(device)
x = x.cuda()

# 模型移到GPU
model = model.to(device)
```

### 二、模型构建

#### 1. nn.Module基础
```python
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, output_dim)
        self.dropout = nn.Dropout(0.5)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x

model = SimpleNet(784, 256, 10)
```

#### 2. 序列模型
```python
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(256, 128),
    nn.ReLU(),
    nn.Linear(128, 10)
)
```

### 三、数据加载

#### 1. Dataset
```python
from torch.utils.data import Dataset

class CustomDataset(Dataset):
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
```

#### 2. DataLoader
```python
from torch.utils.data import DataLoader

dataset = CustomDataset(data, labels)
dataloader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4,
    pin_memory=True
)

for batch_data, batch_labels in dataloader:
    # 训练逻辑
    pass
```

### 四、训练流程

#### 1. 完整训练循环
```python
import torch.optim as optim

# 模型、损失函数、优化器
model = SimpleNet(784, 256, 10).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    
    for batch_data, batch_labels in dataloader:
        batch_data = batch_data.to(device)
        batch_labels = batch_labels.to(device)
        
        # 前向传播
        outputs = model(batch_data)
        loss = criterion(outputs, batch_labels)
        
        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(dataloader):.4f}')
```

#### 2. 验证与测试
```python
model.eval()
correct = 0
total = 0

with torch.no_grad():
    for batch_data, batch_labels in test_loader:
        batch_data = batch_data.to(device)
        batch_labels = batch_labels.to(device)
        
        outputs = model(batch_data)
        _, predicted = torch.max(outputs.data, 1)
        total += batch_labels.size(0)
        correct += (predicted == batch_labels).sum().item()

print(f'Accuracy: {100 * correct / total}%')
```

### 五、模型保存与加载

#### 1. 保存模型
```python
# 保存整个模型
torch.save(model, 'model.pth')

# 保存参数（推荐）
torch.save(model.state_dict(), 'model_params.pth')

# 保存检查点
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}, 'checkpoint.pth')
```

#### 2. 加载模型
```python
# 加载参数
model = SimpleNet(784, 256, 10)
model.load_state_dict(torch.load('model_params.pth'))
model.eval()

# 加载检查点
checkpoint = torch.load('checkpoint.pth')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
```

### 六、常用工具

#### 1. TensorBoard
```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('runs/experiment_1')

for epoch in range(num_epochs):
    # 记录损失
    writer.add_scalar('Loss/train', loss.item(), epoch)
    writer.add_scalar('Accuracy/train', accuracy, epoch)

writer.close()
```

#### 2. 模型参数统计
```python
# 参数数量
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

# 模型摘要
from torchsummary import summary
summary(model, input_size=(1, 28, 28))
```
