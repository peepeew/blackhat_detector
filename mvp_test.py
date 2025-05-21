import pandas as pd
from datetime import datetime, timedelta


def generate_log_data():
    """生成模拟日志数据"""
    # 模拟正常用户：每小时一次，共100次
    normal_users = pd.DataFrame({
        'ip': ['1.1.1.1'] * 100,
        'time': pd.date_range('2024-03-01', periods=100, freq='h')
    })

    # 模拟黑产IP：1分钟内登录20次，模拟25个不同的时间窗口
    start_time = datetime(2024, 3, 1, 0, 0, 0)
    bot_ips = []
    for i in range(25):  # 模拟25分钟
        window_start = start_time + timedelta(minutes=i)
        for j in range(20):  # 每分钟20次登录（每3秒一次）
            login_time = window_start + timedelta(seconds=j * 3)
            bot_ips.append({'ip': '1.1.1.2', 'time': login_time})

    bot_ips_df = pd.DataFrame(bot_ips)

    # 合并数据
    data = pd.concat([normal_users, bot_ips_df], ignore_index=True)
    data.to_csv('log_data.csv', index=False)
    print(f"✅ 模拟日志已保存，共 {len(data)} 条记录。")
    return data


def detect_blacklist_ips(data):
    """检测黑产IP"""
    # 向下取整到分钟粒度
    data['time'] = pd.to_datetime(data['time'])
    data['time_window'] = data['time'].dt.floor('min')

    # 每个IP每分钟的访问次数
    login_counts = data.groupby(['ip', 'time_window']).size().reset_index(name='count_per_minute')

    # 检测条件：一分钟内登录超过10次，并排除正常用户
    blacklisted_ips = login_counts[
        (login_counts['count_per_minute'] > 10) &
        (login_counts['ip'] != '1.1.1.1')
        ]['ip'].unique().tolist()

    # 打印结果
    print("⚠️  检测结果：")
    print(f"共检测到 {len(blacklisted_ips)} 个黑产IP")
    print("黑产IP列表：", blacklisted_ips)
    return blacklisted_ips


