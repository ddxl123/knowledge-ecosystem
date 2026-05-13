# Shell脚本编程

## 核心知识点

### 一、Shell基础

#### 1. Shebang
```bash
#!/bin/bash
# 或
#!/usr/bin/env bash
```

#### 2. 执行脚本
```bash
# 方式1：bash执行
bash script.sh

# 方式2：source执行（当前Shell环境）
source script.sh
. script.sh

# 方式3：直接执行（需要执行权限）
chmod +x script.sh
./script.sh
```

### 二、变量

#### 1. 变量定义
```bash
# 定义变量（等号两边不能有空格）
name="Linux"
version=9

# 使用变量
echo $name
echo ${name}

# 只读变量
readonly PI=3.14159

# 删除变量
unset name
```

#### 2. 特殊变量
```bash
$0    # 脚本名称
$1-$9 # 命令行参数
$#    # 参数个数
$*    # 所有参数（作为一个字符串）
$@    # 所有参数（作为独立字符串）
$?    # 上一个命令的返回值
$$    # 当前进程PID
$!    # 后台运行的最后一个进程PID
```

#### 3. 字符串操作
```bash
str="Hello World"

# 长度
echo ${#str}

# 截取
echo ${str:0:5}     # Hello
echo ${str:6}       # World

# 替换
echo ${str/World/Linux}  # Hello Linux

# 删除
echo ${str#Hello }  # World
echo ${str% World}  # Hello
```

### 三、条件判断

#### 1. if语句
```bash
if [ condition ]; then
    # 代码
elif [ condition ]; then
    # 代码
else
    # 代码
fi
```

#### 2. 条件表达式
```bash
# 字符串比较
[ "$a" = "$b" ]    # 相等
[ "$a" != "$b" ]   # 不等
[ -z "$a" ]        # 为空
[ -n "$a" ]        # 非空

# 数值比较
[ $a -eq $b ]      # 等于
[ $a -ne $b ]      # 不等于
[ $a -gt $b ]      # 大于
[ $a -lt $b ]      # 小于
[ $a -ge $b ]      # 大于等于
[ $a -le $b ]      # 小于等于

# 文件测试
[ -f file ]        # 是文件
[ -d dir ]         # 是目录
[ -e path ]        # 存在
[ -r file ]        # 可读
[ -w file ]        # 可写
[ -x file ]        # 可执行
[ -s file ]        # 非空文件
```

#### 3. 逻辑运算
```bash
[ cond1 ] && [ cond2 ]    # 逻辑与
[ cond1 ] || [ cond2 ]    # 逻辑或
[ ! cond ]                # 逻辑非

# 使用双括号
(( a > b )) && (( a < c ))
[[ -n "$str" && "$str" != "test" ]]
```

### 四、循环

#### 1. for循环
```bash
# 列表循环
for i in 1 2 3 4 5; do
    echo $i
done

# 范围循环
for i in {1..5}; do
    echo $i
done

# C风格循环
for ((i=0; i<5; i++)); do
    echo $i
done

# 遍历文件
for file in /tmp/*.log; do
    echo $file
done
```

#### 2. while循环
```bash
count=0
while [ $count -lt 5 ]; do
    echo $count
    ((count++))
done

# 读取文件
while IFS= read -r line; do
    echo "$line"
done < file.txt
```

#### 3. until循环
```bash
count=0
until [ $count -ge 5 ]; do
    echo $count
    ((count++))
done
```

#### 4. break和continue
```bash
for i in {1..10}; do
    if [ $i -eq 5 ]; then
        break    # 跳出循环
    fi
    if [ $i -eq 3 ]; then
        continue # 跳过本次
    fi
    echo $i
done
```

### 五、函数

#### 1. 函数定义
```bash
# 方式1
function greet() {
    echo "Hello, $1!"
}

# 方式2
greet() {
    echo "Hello, $1!"
}

# 调用函数
greet "World"
```

#### 2. 返回值
```bash
add() {
    local result=$(( $1 + $2 ))
    echo $result    # 通过echo返回
}

# 获取返回值
sum=$(add 3 5)
echo $sum  # 8

# 退出状态
check() {
    if [ -f "$1" ]; then
        return 0  # 成功
    else
        return 1  # 失败
    fi
}

check "/etc/passwd"
echo $?  # 0
```

### 六、数组

```bash
# 定义数组
arr=(apple banana cherry)

# 访问元素
echo ${arr[0]}      # apple
echo ${arr[@]}      # 所有元素
echo ${#arr[@]}     # 数组长度

# 添加元素
arr+=(date elderberry)

# 遍历数组
for item in "${arr[@]}"; do
    echo $item
done
```

### 七、正则表达式

#### 1. 基本语法
```bash
# grep
grep "pattern" file
grep -E "regex" file      # 扩展正则
grep -i "pattern" file    # 忽略大小写
grep -r "pattern" dir     # 递归搜索
grep -v "pattern" file    # 反向匹配

# sed
sed 's/old/new/g' file    # 替换
sed -i 's/old/new/g' file # 原地替换
sed '3d' file             # 删除第3行
sed -n '2,5p' file        # 打印2-5行

# awk
awk '{print $1}' file     # 打印第一列
awk -F: '{print $1}' file # 指定分隔符
awk '$3 > 100' file       # 条件过滤
```

### 八、输入输出

```bash
# 读取输入
read -p "Enter name: " name
read -s -p "Enter password: " pass  # 静默输入

# 重定向
command > file      # 覆盖写入
command >> file     # 追加写入
command < file      # 从文件读取
command 2> error.log # 错误重定向
command &> all.log   # 所有输出重定向

# 管道
command1 | command2
cat file | grep "pattern" | sort
```
