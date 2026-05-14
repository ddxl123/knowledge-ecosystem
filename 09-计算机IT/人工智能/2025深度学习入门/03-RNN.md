# 循环神经网络（RNN）


## 收集指南

> ⚠️ **严格范围限定：** 仅收集本章（第3章 RNN）相关内容，禁止跨章节引用。

### 条目描述
本文件是《2025深度学习入门》中关于「RNN」的知识原子文件，属于人工智能方向。

### 知识结构
- RNN 基础
- LSTM 与 GRU
- 双向 RNN
- 应用场景
- 序列建模

### 待收集原子知识点
- RNN 结构与梯度问题
- LSTM 门控机制
- GRU 简化设计
- 双向/深层 RNN
- 文本分类/序列标注

## 核心知识点

### 一、RNN 基础

```python
import torch
import torch.nn as nn

# 基础 RNN
rnn = nn.RNN(
    input_size=128,     # 输入特征维度
    hidden_size=256,    # 隐藏状态维度
    num_layers=2,       # RNN 层数
    batch_first=True,   # 输入形状 (batch, seq, feature)
    dropout=0.3,
    bidirectional=False
)

# 输入形状: (batch_size, seq_len, input_size)
x = torch.randn(32, 50, 128)  # batch=32, 序列长度=50
output, hidden = rnn(x)
# output: (32, 50, 256) 所有时间步的输出
# hidden: (2, 32, 256) 最后时间步的隐藏状态
```

- **RNN 的问题：**
  - 梯度消失：长序列中梯度指数衰减，难以学习长距离依赖
  - 梯度爆炸：梯度指数增长，参数更新不稳定
  - 解决方案：LSTM、GRU、梯度裁剪

### 二、LSTM（长短期记忆）

```python
# LSTM 单元结构
# 遗忘门: f = σ(W_f · [h_{t-1}, x_t] + b_f)
# 输入门: i = σ(W_i · [h_{t-1}, x_t] + b_i)
# 候选值: C̃ = tanh(W_C · [h_{t-1}, x_t] + b_C)
# 细胞状态: C_t = f * C_{t-1} + i * C̃
# 输出门: o = σ(W_o · [h_{t-1}, x_t] + b_o)
# 隐藏状态: h_t = o * tanh(C_t)

lstm = nn.LSTM(
    input_size=128,
    hidden_size=256,
    num_layers=2,
    batch_first=True,
    dropout=0.3,
    bidirectional=True  # 双向 LSTM
)

x = torch.randn(32, 50, 128)
output, (hidden, cell) = lstm(x)
# output: (32, 50, 512) 双向时 hidden_size * 2
# hidden: (4, 32, 256) num_layers * num_directions
# cell: (4, 32, 256) 细胞状态
```

### 三、GRU（门控循环单元）

```python
# GRU 是 LSTM 的简化版本
# 更新门: z = σ(W_z · [h_{t-1}, x_t])
# 重置门: r = σ(W_r · [h_{t-1}, x_t])
# 候选值: h̃ = tanh(W · [r * h_{t-1}, x_t])
# 隐藏状态: h_t = (1 - z) * h_{t-1} + z * h̃

gru = nn.GRU(
    input_size=128,
    hidden_size=256,
    num_layers=2,
    batch_first=True,
    bidirectional=True
)

output, hidden = gru(x)
# GRU 没有细胞状态，参数比 LSTM 少约 25%
```

### 四、序列模型应用

```python
# 文本分类模型
class TextClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers=2,
                           batch_first=True, bidirectional=True, dropout=0.3)
        self.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(hidden_dim * 2, num_classes)  # 双向 * 2
        )
    
    def forward(self, x):
        x = self.embedding(x)           # (batch, seq) → (batch, seq, embed)
        output, (hidden, _) = self.lstm(x)
        # 取最后一层双向的隐藏状态拼接
        hidden = torch.cat([hidden[-2], hidden[-1]], dim=1)
        return self.fc(hidden)

# 序列标注（NER/POS Tagging）
class SequenceTagger(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_tags):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, num_tags)
        self.crf = CRF(num_tags)  # CRF 层提升标注一致性
    
    def forward(self, x):
        x = self.embedding(x)
        output, _ = self.lstm(x)
        emissions = self.fc(output)
        return emissions
```

### 五、LSTM vs GRU 选择

- **LSTM：** 适合需要精细控制记忆的场景，长序列依赖
- **GRU：** 参数少、训练快，适合数据量较少的场景
- **实践建议：** 先试 GRU，效果不好再换 LSTM
- **当前趋势：** Transformer 在大多数 NLP 任务中已替代 RNN
