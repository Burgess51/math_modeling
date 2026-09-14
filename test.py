print("hello world")
import os
# 把common文件夹加入路径，才能导入公共工具
print(os.path.join(os.path.dirname(__file__), 'jiangnan/common'))