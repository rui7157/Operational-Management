#!/usr/bin/env bash

# 删除所有文件
echo echo "正在删除目录 /var/www/cdms/"

rm -rf /var/www/cdms

# 获取最新代码
echo "获取最新代码"
git clone git@192.168.2.222:/home/git/cdms.git /var/www/cdms

# 创建 Python 虚拟环境

if [ ! -d "/var/www/venv" ]; then
  echo "创建Python虚拟环境"
  virtualenv /var/www/venv
  echo "正在设置目录权限"
  chown www-data:www-data /var/www/venv -R
  chmod 777 /var/www/venv -R
fi

# 导入 Python 模块
if [ ! -d "/var/www/venv" ]; then
    echo "导入 Python 模块"
    . /var/www/venv/bin/activate
    su bayonet pip install -r requirements.txt
fi

if [ ! -d "/var/www/cdms" ]; then
  echo "正在设置目录权限"
  chown www-data:www-data /var/www/cdms/ -R
  chmod 777 /var/www/cdms -R
fi


# 重启 uwsig 服务
echo "正在重启服务"
restart uwsig

# 设置 Python 根目录
BASE=/home/bayonet/Codes/Blog/venv/bin
# 启动Python 脚本
$BASE/python /home/bayonet/cdms/uwsig_restart.py

echo "完成！Bye"