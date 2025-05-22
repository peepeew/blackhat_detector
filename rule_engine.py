import pandas as pd
def detect_high_freq(data, config):
    data['time'] = pd.to_datetime(data['time'])
    data['time_window'] = data['time'].dt.floor('min')
    grouped = data.groupby(['ip', 'time_window']).size().reset_index(name='count')

    threshold = config['threshold_per_minute']
    whitelist = config.get('whitelist_ips', [])
    suspects = grouped[grouped['count'] > threshold]['ip'].unique()
    suspects = [ip for ip in suspects if ip not in whitelist]
    return suspects

def detect_path_probe(data, config):
    # 确保路径字段存在
    if 'path' not in data.columns:
        return []
    sensitive_paths = set(config.get('sensitive_paths', []))
    threshold = config.get('threshold', 3)
    whitelist = config.get('whitelist_ips', [])

    # 统计每个 IP 请求了多少个不同的敏感路径
    filtered = data[data['path'].isin(sensitive_paths)]
    grouped = filtered.groupby('ip')['path'].nunique().reset_index()
    suspects = grouped[grouped['path'] >= threshold]['ip'].unique()
    suspects = [ip for ip in suspects if ip not in whitelist]
    return suspects

def detect_path_probe_freq(data, config):
    # 确保路径字段存在
    if 'path' not in data.columns:
        return []

    sensitive_paths = set(config.get('sensitive_paths', []))
    threshold = config.get('threshold', 10)
    whitelist = config.get('whitelist_ips', [])

        # 统计每个 IP 对敏感路径的访问总次数
    filtered = data[data['path'].isin(sensitive_paths)]
    grouped = filtered.groupby('ip').size().reset_index(name='count')
    suspects = grouped[grouped['count'] >= threshold]['ip'].unique()
    suspects = [ip for ip in suspects if ip not in whitelist]
    return suspects
