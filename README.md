"""
Blackhat Detector 是一个用于检测黑产高频行为（如暴力破解、刷单脚本等）的轻量级规则检测系统。
支持可配置规则和伪实时检测。
"""

## 📦 项目结构

```
blackhat_detector/
├── log_generator.py         # 生成模拟日志（正常 + 黑产IP）
├── config/
│   ├── rules.yaml           # 检测规则配置（YAML 格式）
│   └── whitelist.txt        # 白名单 IP（不被检测）
├── rule_engine.py           # 高频检测规则引擎模块
├── detect.py                # 主检测程序，输出 blacklist.json
├── realtime_simulator.py    # 伪实时模拟器（每5秒检测一次）
├── outputs/
│   ├── log_data.csv         # 日志数据文件
│   └── blacklist.json       # 检测结果输出
└── utils.py                 # 预留工具模块
```

## 🚀 使用方式

### 1. 生成模拟数据
```bash
python log_generator.py
```

### 2. 执行一次检测（静态）
```bash
python detect.py
```

### 3. 启动伪实时检测（每5秒运行一次）
```bash
python realtime_simulator.py
```

## 🛠️ 自定义规则
编辑 `config/rules.yaml` 来调整检测逻辑，例如：
```yaml
rules:
  - name: high_freq_login
    type: frequency
    threshold_per_minute: 10
    whitelist: ./config/whitelist.txt
```