# Linux Shell 编程


## 收集指南

> ⚠️ **严格范围限定：** 仅收集本章（第4章 Shell）相关内容，禁止跨章节引用。

### 条目描述
本文件是《2025鸟哥的Linux私房菜》中关于「Shell」的知识原子文件，属于Linux方向。

### 知识结构
- Shell 基础语法
- 变量与数据类型
- 流程控制
- 函数
- 实用脚本

### 待收集原子知识点
- Bash 语法与脚本结构
- 变量/数组/字符串操作
- if/for/while/case
- 函数定义与参数
- 文本处理（awk/sed/grep）

## 核心知识点

### 一、Shell 脚本基础

```bash
#!/bin/bash
# 脚本开头指定解释器

# 变量
name="Linux"
echo "Hello, $name"
echo "Hello, ${name}!"    # 花括号明确边界

# 特殊变量
$0    # 脚本名称
$1-$9 # 位置参数
$#    # 参数个数
$@    # 所有参数（数组）
$*    # 所有参数（字符串）
$?    # 上一条命令的退出状态
$$    # 当前进程 PID

# 命令替换
current_date=$(date +%Y-%m-%d)
file_count=$(ls | wc -l)

# 算术运算
result=$((10 + 5))
result=$((a * b))
```

### 二、条件判断

```bash
# if 语句
if [ "$age" -ge 18 ]; then
    echo "成年人"
elif [ "$age" -ge 12 ]; then
    echo "青少年"
else
    echo "儿童"
fi

# 文件测试
if [ -f "$file" ]; then echo "文件存在"; fi
if [ -d "$dir" ]; then echo "目录存在"; fi
if [ -r "$file" ]; then echo "可读"; fi
if [ -w "$file" ]; then echo "可写"; fi
if [ -x "$file" ]; then echo "可执行"; fi
if [ -s "$file" ]; then echo "非空文件"; fi

# 字符串比较
if [ "$str1" = "$str2" ]; then echo "相等"; fi
if [ -z "$str" ]; then echo "空字符串"; fi
if [ -n "$str" ]; then echo "非空字符串"; fi

# case 语句
case "$1" in
    start)   echo "启动服务" ;;
    stop)    echo "停止服务" ;;
    restart) echo "重启服务" ;;
    *)       echo "用法: $0 {start|stop|restart}" ;;
esac
```

### 三、循环

```bash
# for 循环
for i in 1 2 3 4 5; do
    echo $i
done

for i in $(seq 1 10); do
    echo $i
done

for file in *.txt; do
    echo "Processing $file"
done

# C 风格 for
for ((i=0; i<10; i++)); do
    echo $i
done

# while 循环
count=0
while [ $count -lt 5 ]; do
    echo $count
    ((count++))
done

# 读取文件
while IFS= read -r line; do
    echo "$line"
done < /etc/passwd

# until 循环
until [ $count -ge 10 ]; do
    ((count++))
done
```

### 四、函数

```bash
# 函数定义
greet() {
    local name=$1    # local 声明局部变量
    echo "Hello, $name!"
    return 0
}

greet "World"        # 调用函数

# 带返回值
add() {
    local result=$(($1 + $2))
    echo $result     # 通过 echo 输出结果
}

sum=$(add 3 5)       # 用命令替换获取结果
echo "3 + 5 = $sum"

# 参数检查
validate_input() {
    if [ -z "$1" ]; then
        echo "Error: 参数不能为空" >&2
        return 1
    fi
}
```

### 五、文本处理三剑客

```bash
# grep（文本搜索）
grep "error" /var/log/syslog
grep -r "TODO" ./src/           # 递归搜索
grep -i "hello" file.txt        # 忽略大小写
grep -n "pattern" file.txt      # 显示行号
grep -c "error" log.txt         # 统计匹配行数
grep -E "regex|pattern" file    # 扩展正则

# sed（流编辑器）
sed 's/old/new/' file.txt             # 替换第一个匹配
sed 's/old/new/g' file.txt            # 替换所有匹配
sed -i 's/old/new/g' file.txt        # 原地修改
sed '3d' file.txt                     # 删除第3行
sed '/pattern/d' file.txt             # 删除匹配行
sed -n '5,10p' file.txt              # 打印5-10行

# awk（文本处理）
awk '{print $1, $3}' file.txt        # 打印第1和第3列
awk -F: '{print $1}' /etc/passwd     # 指定分隔符
awk '$3 > 100' file.txt              # 条件过滤
awk '{sum+=$1} END {print sum}' file # 求和
awk 'NR==5' file.txt                 # 第5行
```
