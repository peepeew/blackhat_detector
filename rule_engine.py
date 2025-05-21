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