"""
伪实时检测模拟器：每5秒拉一次log_data.csv并执行检测。
"""
import time, os
from detect import *

while True:
    print("[实时模拟] 正在执行检测...")
    os.system("python detect.py")
