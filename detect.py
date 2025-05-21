import yaml, json
import pandas as pd
from rule_engine import detect_high_freq

with open('./config/rules.yaml', encoding='utf-8') as f:
    rules = yaml.safe_load(f)['rules']

with open('./config/whitelist.txt', encoding='utf-8') as f:
    whitelist_ips = [line.strip() for line in f.readlines()]

data = pd.read_csv('./outputs/log_data.csv')
result = {}
for rule in rules:
    if rule['type'] == 'frequency':
        rule['whitelist_ips'] = whitelist_ips
        result[rule['name']] = detect_high_freq(data, rule)

# 确保输出目录存在
import os
os.makedirs('./outputs', exist_ok=True)

with open('./outputs/blacklist.json', 'w') as f:
    json.dump(result, f, indent=2)
print("✅ 黑产检测完成，结果已保存到 blacklist.json")