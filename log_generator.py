"""
用于生成模拟日志数据，包括正常用户行为和模拟黑产IP高频行为。
"""
import pandas as pd
from datetime import datetime, timedelta
import os

def generate_log_data():
    normal_users = pd.DataFrame({
        'ip': ['1.1.1.1'] * 100,
        'time': pd.date_range('2024-03-01', periods=100, freq='h')
    })

    start_time = datetime(2024, 3, 1, 0, 0, 0)
    bot_ips = []
    for i in range(25):
        window_start = start_time + timedelta(minutes=i)
        for j in range(20):
            login_time = window_start + timedelta(seconds=j * 3)
            bot_ips.append({'ip': '1.1.1.2', 'time': login_time})

    bot_ips_df = pd.DataFrame(bot_ips)
    data = pd.concat([normal_users, bot_ips_df], ignore_index=True)

    # 确保输出目录存在
    os.makedirs('./outputs', exist_ok=True)

    data.to_csv('./outputs/log_data.csv', index=False)
    print(f"✅ 模拟日志已保存，共 {len(data)} 条记录。")
    return data

if __name__ == "__main__":
    generate_log_data()