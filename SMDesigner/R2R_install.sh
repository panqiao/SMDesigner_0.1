#!/bin/bash

# 创建一个子目录用于存放下载的文件
mkdir -p R2R
cd R2R

# 下载 R2R
echo "download R2R..."
wget -O R2R-1.0.6.tgz https://sourceforge.net/projects/weinberg-r2r/files/R2R-1.0.6.tgz/download

# 解压文件
tar -zxvf R2R-1.0.6.tgz

# 编译和安装 R2R
echo "install R2R..."
cd R2R-1.0.6
./configure 
make
make install
