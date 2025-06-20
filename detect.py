import yaml, json
import pandas as pd
import os

# 引入所有规则函数
from rule_engine import (
    detect_high_freq,
    detect_path_probe,
    detect_path_probe_freq,
    detect_ua_check,
    detect_referer_check,
    detect_slow_request
)

# 加载规则配置
with open('./config/rules.yaml', encoding='utf-8') as f:
    rules = yaml.safe_load(f)['rules']

# 加载白名单 IP
with open('./config/whitelist.txt', encoding='utf-8') as f:
    whitelist_ips = [line.strip() for line in f.readlines()]

# 加载结构化日志数据
data = pd.read_csv('./outputs/log_data_structured.csv')

# 执行所有规则检测
result = {}
for rule in rules:
    rule_type = rule['type']
    rule['whitelist_ips'] = whitelist_ips

    if rule_type == 'frequency':
        result[rule['name']] = detect_high_freq(data, rule)
    elif rule_type == 'path_probe':
        result[rule['name']] = detect_path_probe(data, rule)
    elif rule_type == 'path_probe_freq':
        result[rule['name']] = detect_path_probe_freq(data, rule)
    elif rule_type == 'ua_check':
        result[rule['name']] = detect_ua_check(data, rule)
    elif rule_type == 'referer_check':
        result[rule['name']] = detect_referer_check(data, rule)
    elif rule_type == 'slow_request':
        result[rule['name']] = detect_slow_request(data, rule)
    else:
        print(f"⚠️ 未知规则类型: {rule_type}")

# 保存检测结果
os.makedirs('./outputs', exist_ok=True)
with open('./outputs/blacklist.json', 'w') as f:
    json.dump(result, f, indent=2)

print("✅ 黑产检测完成，结果已保存到 blacklist.json")
