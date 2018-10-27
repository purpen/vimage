#!/bin/sh
#
# 同步git代码库
#
# @example: /path/to/sync_upgrade.sh
#

unset GIT_DIR

# 项目根目录
PROJECT_ROOT="/opt/project/vimage"
LOG_FILE="/opt/project/vimage/gitsync.log"

echo -e "\n=================  `date +%Y-%m-%d\ %H:%M:%S`  ===============\n" >> $LOG_FILE 2>&1

# 进入项目目录
cd $PROJECT_ROOT

# 这里直接丢弃工作区的内容，防止出现一些奇怪的错误。项目目录只做pull，不在这里修改东西
git reset --hard

# 先拉取，再合并
git pull origin master

# 切换环境
source venv/bin/activate

# 安装依赖包
pip3 install -r requirements.txt


echo "=========================== ok ===================="  >> $LOG_FILE 2>&1