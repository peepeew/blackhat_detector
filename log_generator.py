import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

def random_ip_list(n):
    return [fake.ipv4() for _ in range(n)]

methods = ['GET', 'POST']
referers = ['-', 'https://www.google.com/', 'https://example.com/page', 'https://baidu.com/search']
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'curl/7.68.0',
    'python-requests/2.25.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
]
protocols = ['HTTP/1.0', 'HTTP/1.1', 'HTTP/2.0']
hosts = ['api.example.com', 'shop.example.com']

def generate_rows(ip, path, count, start_time, freq_seconds=60):
    rows = []
    for i in range(count):
        log_time = start_time + timedelta(seconds=i * freq_seconds + random.randint(0, 3))
        row = {
            'ip': ip,
            'time': log_time,
            'path': path,
            'method': 'POST' if path in ['/login', '/register'] else random.choice(methods),
            'status': random.choice([200, 401, 403]) if path == '/login' else 200,
            'referer': random.choice(referers),
            'user_agent': random.choice(user_agents),
            'x_forwarded_for': random.choice(['-', fake.ipv4(), fake.ipv4()]),
            'request_time': round(random.uniform(0.05, 1.5), 3),
            'protocol': random.choice(protocols),
            'host': random.choice(hosts)
        }
        rows.append(row)
    return rows

def generate_log_data():
    all_logs = []
    start_time = datetime(2024, 3, 1, 0, 0, 0)

    # 正常访问者（20 个 IP，每人访问 20~40 次）
    normal_ips = random_ip_list(20)
    for ip in normal_ips:
        count = random.randint(20, 40)
        all_logs.extend(generate_rows(ip, '/home', count, start_time, freq_seconds=300))  # 每 5 分钟一次

    # 暴力破解（15 个 IP，每人登录爆破 40 次）
    attack_ips = random_ip_list(15)
    for ip in attack_ips:
        all_logs.extend(generate_rows(ip, '/login', 40, start_time, freq_seconds=3))

    # 路径探测（15 个 IP，每个 IP 扫描 3~4 个路径，每个路径访问 5 次）
    sensitive_paths = ['/admin', '/phpmyadmin', '/.git', '/config', '/backup.zip']
    scan_ips = random_ip_list(15)
    for ip in scan_ips:
        paths = random.sample(sensitive_paths, k=random.randint(3, 4))
        for path in paths:
            all_logs.extend(generate_rows(ip, path, 5, start_time, freq_seconds=15))

    # 注册刷号攻击（10 个 IP，每人访问 /register 30 次）
    spam_ips = random_ip_list(10)
    for ip in spam_ips:
        all_logs.extend(generate_rows(ip, '/register', 30, start_time, freq_seconds=10))

    # 合并数据
    full_data = pd.DataFrame(all_logs)
    full_data = full_data.sort_values(by='time').reset_index(drop=True)

    # 输出到 CSV
    full_data.to_csv('./outputs/log_data_structured.csv', index=False)
    print(f"✅ 日志生成完成，共 {len(full_data)} 条记录，IP 数量：{full_data['ip'].nunique()} 个。")

if __name__ == "__main__":
    generate_log_data()
