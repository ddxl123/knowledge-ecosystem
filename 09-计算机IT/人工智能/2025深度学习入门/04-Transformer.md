# Transformer 架构


## 收集指南

> ⚠️ **严格范围限定：** 仅收集本章（第4章 Transformer）相关内容，禁止跨章节引用。

### 条目描述
本文件是《2025深度学习入门》中关于「Transformer」的知识原子文件，属于人工智能方向。

### 知识结构
- 注意力机制
- 自注意力与多头注意力
- Transformer 结构
- 位置编码
- 预训练模型

### 待收集原子知识点
- Scaled Dot-Product Attention
- Multi-Head Attention
- Encoder-Decoder 架构
- 位置编码方式
- BERT/GPT 系列

## 核心知识点

### 一、注意力机制

```python
import torch
import torch.nn as nn
import math

# Scaled Dot-Product Attention
def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q: (batch, heads, seq_q, d_k)
    K: (batch, heads, seq_k, d_k)
    V: (batch, heads, seq_k, d_v)
    """
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    
    attention_weights = torch.softmax(scores, dim=-1)
    output = torch.matmul(attention_weights, V)
    return output, attention_weights
```

### 二、多头注意力

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model=512, num_heads=8):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
    
    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)
        
        # 线性变换并分头
        Q = self.W_q(Q).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(K).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(V).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # 注意力计算
        attn_output, attn_weights = scaled_dot_product_attention(Q, K, V, mask)
        
        # 拼接并线性变换
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
        return self.W_o(attn_output)
```

### 三、Transformer 结构

```python
class TransformerBlock(nn.Module):
    def __init__(self, d_model=512, num_heads=8, d_ff=2048, dropout=0.1):
        super().__init__()
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout)
        )
    
    def forward(self, x, mask=None):
        # 自注意力 + 残差连接 + 层归一化
        attn_output = self.attention(x, x, x, mask)
        x = self.norm1(x + attn_output)
        # 前馈网络 + 残差连接 + 层归一化
        ffn_output = self.ffn(x)
        x = self.norm2(x + ffn_output)
        return x
```

### 四、位置编码

```python
# 正弦位置编码
class PositionalEncoding(nn.Module):
    def __init__(self, d_model=512, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                           -(math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0))
    
    def forward(self, x):
        return x + self.pe[:, :x.size(1)]
```

### 五、预训练模型

- **BERT（Encoder-only）：**
  - 双向注意力，理解上下文
  - 适合：文本分类、NER、问答
  - 预训练任务：MLM（掩码语言模型）+ NSP

- **GPT（Decoder-only）：**
  - 单向注意力（因果掩码）
  - 适合：文本生成、对话
  - 预训练任务：下一个词预测

- **T5（Encoder-Decoder）：**
  - 统一框架，所有任务转为文本到文本
  - 适合：翻译、摘要、问答

- **2025 趋势：**
  - 大语言模型（LLM）：GPT-4、Claude、Llama 3
  - 多模态模型：图文理解与生成
  - 高效架构：FlashAttention、MoE（混合专家）
