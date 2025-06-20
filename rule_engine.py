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

def detect_ua_check(data, config):
    if 'user_agent' not in data.columns:
        return []

    bad_keywords = config.get('bad_ua_keywords', [])
    threshold = config.get('threshold', 3)
    whitelist = config.get('whitelist_ips', [])

    def is_bad_ua(ua):
        return any(keyword.lower() in str(ua).lower() for keyword in bad_keywords)

    data['is_bad_ua'] = data['user_agent'].apply(is_bad_ua)
    grouped = data[data['is_bad_ua']].groupby('ip').size().reset_index(name='count')
    suspects = grouped[grouped['count'] >= threshold]['ip'].unique()
    return [ip for ip in suspects if ip not in whitelist]

def detect_referer_check(data, config):
    if 'referer' not in data.columns:
        return []

    target_path = config.get('target_path', '/login')
    expected = set(config.get('expected_referers', []))
    threshold = config.get('threshold', 5)
    allow_empty = config.get('allow_empty', False)
    whitelist = config.get('whitelist_ips', [])

    def is_bad_referer(ref):
        if not ref or ref == '-':
            return not allow_empty
        return ref not in expected

    filtered = data[data['path'] == target_path].copy()
    filtered['bad_ref'] = filtered['referer'].apply(is_bad_referer)
    grouped = filtered[filtered['bad_ref']].groupby('ip').size().reset_index(name='count')
    suspects = grouped[grouped['count'] >= threshold]['ip'].unique()
    return [ip for ip in suspects if ip not in whitelist]

def detect_slow_request(data, config):
    if 'request_time' not in data.columns:
        return []

    threshold_sec = config.get('threshold_seconds', 1.0)
    count_threshold = config.get('count_threshold', 5)
    whitelist = config.get('whitelist_ips', [])

    filtered = data[data['request_time'] >= threshold_sec]
    grouped = filtered.groupby('ip').size().reset_index(name='count')
    suspects = grouped[grouped['count'] >= count_threshold]['ip'].unique()
    return [ip for ip in suspects if ip not in whitelist]

