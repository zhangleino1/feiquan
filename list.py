#!/usr/bin/python3
import requests
import threading
import json
from bs4 import BeautifulSoup
import time
from urllib.parse import quote  # 导入quote而不是urlencode
import os

urlbase = 'https://github.com/zhangleino1/feiquan/blob/main/2024/'

# 遍历rootpath目录
rootpath = 'D:/work/dream/feiquan/2024'
for root, dirs, files in os.walk(rootpath):
    for file in files:
        if file.endswith('.md'):
            # 使用quote函数对file进行编码
            fileurl = urlbase + quote(file)
            on = '- ['+file+']('+fileurl+')'
            print(on)
