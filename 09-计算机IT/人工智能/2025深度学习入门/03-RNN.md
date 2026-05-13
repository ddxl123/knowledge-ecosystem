# 循环神经网络（RNN）

## 核心知识点

### 一、RNN基础

#### 1. 基本结构
```
输入序列: x₁, x₂, ..., xₜ
隐藏状态: h₁, h₂, ..., hₜ
输出序列: y₁, y₂, ..., yₜ

hₜ = tanh(Wₓₕxₜ + Wₕₕhₜ₋₁ + bₕ)
yₜ = Wₕᵧhₜ + bᵧ
```

#### 2. PyTorch实现
```python
import torch
import torch.nn as nn

# 基本RNN
rnn = nn.RNN(
    input_size=10,      # 输入特征维度
    hidden_size=20,     # 隐藏状态维度
    num_layers=2,       # 层数
    batch_first=True    # 输入格式: (batch, seq_len, features)
)

# 输入: (batch, seq_len, input_size)
x = torch.randn(32, 50, 10)
output, h_n = rnn(x)
# output: (batch, seq_len, hidden_size)
# h_n: (num_layers, batch, hidden_size)
```

### 二、LSTM（长短期记忆网络）

#### 1. 核心思想
```
遗忘门: fₜ = σ(Wf·[hₜ₋₁, xₜ] + bf)
输入门: iₜ = σ(Wi·[hₜ₋₁, xₜ] + bi)
候选值: C̃ₜ = tanh(Wc·[hₜ₋₁, xₜ] + bc)
细胞状态: Cₜ = fₜ * Cₜ₋₁ + iₜ * C̃ₜ
输出门: oₜ = σ(Wo·[hₜ₋₁, xₜ] + bo)
隐藏状态: hₜ = oₜ * tanh(Cₜ)
```

#### 2. PyTorch实现
```python
lstm = nn.LSTM(
    input_size=10,
    hidden_size=20,
    num_layers=2,
    batch_first=True,
    dropout=0.2,
    bidirectional=True  # 双向LSTM
)

x = torch.randn(32, 50, 10)
output, (h_n, c_n) = lstm(x)
# output: (batch, seq_len, hidden_size * 2)  双向
# h_n: (num_layers * 2, batch, hidden_size)
# c_n: (num_layers * 2, batch, hidden_size)
```

### 三、GRU（门控循环单元）

#### 1. 结构特点
```
更新门: zₜ = σ(Wz·[hₜ₋₁, xₜ])
重置门: rₜ = σ(Wr·[hₜ₋₁, xₜ])
候选值: h̃ₜ = tanh(W·[rₜ * hₜ₋₁, xₜ])
隐藏状态: hₜ = (1 - zₜ) * hₜ₋₁ + zₜ * h̃ₜ
```

#### 2. PyTorch实现
```python
gru = nn.GRU(
    input_size=10,
    hidden_size=20,
    num_layers=2,
    batch_first=True
)

x = torch.randn(32, 50, 10)
output, h_n = gru(x)
```

### 四、序列模型应用

#### 1. 文本分类
```python
class TextClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, num_classes)
    
    def forward(self, x):
        x = self.embedding(x)  # (batch, seq_len, embed_dim)
        output, (h_n, _) = self.lstm(x)
        # 使用最后一个时间步的隐藏状态
        x = h_n[-1]  # (batch, hidden_dim)
        x = self.fc(x)
        return x
```

#### 2. 序列生成
```python
class SeqGenerator(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)
    
    def forward(self, x, hidden=None):
        x = self.embedding(x)
        output, hidden = self.lstm(x, hidden)
        x = self.fc(output)
        return x, hidden
```

### 五、RNN变体与技巧

#### 1. 双向RNN
```python
# 从左到右 + 从右到左
bi_lstm = nn.LSTM(input_size, hidden_size, bidirectional=True)
# 输出维度: hidden_size * 2
```

#### 2. 多层RNN
```python
# 堆叠多层
multi_lstm = nn.LSTM(input_size, hidden_size, num_layers=3, dropout=0.3)
```

#### 3. 序列填充与打包
```python
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

# 打包变长序列
packed = pack_padded_sequence(x, lengths, batch_first=True, enforce_sorted=False)
output, h_n = lstm(packed)
output, _ = pad_packed_sequence(output, batch_first=True)
```

### 六、RNN的局限性

#### 1. 长距离依赖问题
- 梯度消失/梯度爆炸
- 难以捕捉长距离依赖
- LSTM/GRU部分缓解，但未完全解决

#### 2. 序列处理限制
- 无法并行处理序列
- 训练速度慢
- Transformer架构的出现解决了这些问题
