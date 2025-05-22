import pandas as pd
from datetime import datetime, timedelta

def generate_log_data():
    """
    生成模拟日志数据，包括：
    1. 正常用户访问
    2. 高频暴力破解（频率规则命中）
    3. 多路径探测（多路径规则命中）
    4. 单路径刷接口（路径频率规则命中）
    """
    all_logs = []

    # 1️⃣ 正常用户访问（每小时访问一次）
    normal_users = pd.DataFrame({
        'ip': ['1.1.1.1'] * 100,
        'time': pd.date_range('2024-03-01', periods=100, freq='h'),
        'path': ['/home'] * 100
    })
    all_logs.append(normal_users)

    # 2️⃣ 高频访问：1分钟内访问20次（暴力破解类）
    start_time = datetime(2024, 3, 1, 0, 0, 0)
    bot_ips = [
        {
            'ip': '1.1.1.2',
            'time': start_time + timedelta(minutes=i) + timedelta(seconds=j * 3),
            'path': '/login'
        }
        for i in range(25)  # 25个分钟窗口
        for j in range(20)  # 每分钟访问20次
    ]
    all_logs.append(pd.DataFrame(bot_ips))

    # 3️⃣ 多路径探测：访问多个敏感路径
    path_scan = [
        {
            'ip': '1.1.1.3',
            'time': start_time + timedelta(minutes=i),
            'path': path
        }
        for path in ['/admin', '/login', '/phpmyadmin']
        for i in range(5)
    ]
    all_logs.append(pd.DataFrame(path_scan))

    # 4️⃣ 单路径高频刷号攻击：重复访问同一路径
    register_spammer = [
        {
            'ip': '1.1.1.4',
            'time': start_time + timedelta(seconds=i * 5),
            'path': '/login'
        }
        for i in range(15)
    ]
    all_logs.append(pd.DataFrame(register_spammer))

    # 合并所有数据
    full_data = pd.concat(all_logs, ignore_index=True)

    # 输出为 CSV
    full_data.to_csv('./outputs/log_data.csv', index=False)
    print(f"✅ 测试路径日志已生成，共 {len(full_data)} 条记录。")

if __name__ == "__main__":
    generate_log_data()
