# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概览

**加密底部追踪器** (Crypto Bottom Tracker) - 用于跟踪和识别加密货币市场潜在底部信号的 Python 工具。监控五大关键指标（市场情绪、矿工投降、黑天鹅事件、宏观环境、流动性），输出红/黄/绿灯仪表盘，并自动生成可视化图表和 Telegram 推送。

## 核心命令

### 运行追踪器

```bash
# 执行一次（生成仪表盘 + 推送到 Telegram）
python3 crypto-bottom-tracker.py

# 查看网页仪表盘
open index.html
# 或通过 HTTP 服务器
python3 -m http.server 8000  # 然后打开 http://localhost:8000
```

### 定时执行（macOS Launchd）

```bash
# 设置每天 08:00 自动执行
python3 setup_timer.py

# 查看状态
launchctl list | grep com.crypto.bottom-tracker

# 手动触发
launchctl start com.crypto.bottom-tracker

# 停止/卸载
launchctl unload ~/Library/LaunchAgents/com.crypto.bottom-tracker.plist

# 查看日志
tail -f tracker.log
```

## 架构设计

### 数据流程

1. **数据采集** (`crypto-bottom-tracker.py:69-116`):
   - 恐惧贪婪指数：从 CoinGecko API 获取
   - 比特币哈希率：从 Blockchain.info API 获取
   - 黑天鹅评分 (BSS)：基于 180 天价格/成交量数据计算
   - 宏观数据 (VIX, TNX)：优先使用 Polygon.io API，失败时回退到 yfinance
   - 稳定币占比 (SSR)：从 CoinGecko 获取

2. **指标计算** (`crypto-bottom-tracker.py:82-117`):
   - 市场极度恐慌：FGI ≤20（绿灯），≤35（黄灯），>35（红灯）
   - 矿工投降：哈希率变化阈值判断
   - 黑天鹅强度：BSS 加权评分（价格冲击、成交量激增、恐慌峰值）
   - 宏观股市熊市：VIX（60% 权重）+ ERP 计算（40% 权重）
   - 流动性恢复：SSR >= 8%（绿灯），>= 6%（黄灯），<6%（红灯）

3. **输出生成** (`crypto-bottom-tracker.py:124-163`):
   - `web_data.json`：网页仪表盘的 JSON 数据
   - `dashboard.png`：可视化指标仪表盘（保存到项目目录）
   - Telegram：文字报告 + 图片推送

### 关键文件

- `crypto-bottom-tracker.py`：主程序脚本，包含所有逻辑
- `index.html`：独立网页仪表盘（每 30 秒自动刷新）
- `setup_timer.py`：macOS Launchd 配置生成器
- `web_data.json`：生成的网页界面数据文件
- `dashboard.png`：生成的指标仪表盘图片

### 数据源与缓存

**混合数据策略**：
- **主数据源**：Polygon.io API 获取 VIX/TNX（有 API 密钥时无限流）
- **备用数据源**：yfinance，带 6 小时缓存（`.bss_cache.txt`、`macro_cache.json`）
- **永久免费**：CoinGecko（加密货币数据）、Blockchain.info（哈希率）

**智能缓存**：6 小时缓存机制防止 yfinance API 限流，同时保持数据合理新鲜度。

### API 配置

需在 `crypto-bottom-tracker.py:9-11` 配置以下密钥：
- `TELEGRAM_BOT_TOKEN`：从 @BotFather 获取
- `TELEGRAM_CHAT_ID`：从 @userinfobot 获取
- `POLYGON_API_KEY`：从 polygon.io 获取（可选但推荐）

## 五大指标逻辑

### 1. 市场极度恐慌（FGI）
- 绿灯：FGI ≤ 20（极度恐慌，强烈底部信号）
- 黄灯：FGI ≤ 35（偏恐慌）
- 红灯：> 35（正常/乐观）

### 2. 矿工投降（哈希率）
- 绿灯：< -18%（强投降）
- 黄灯：< -5%（轻度投降）
- 红灯：≥ -5%（稳定/上涨）

### 3. 黑天鹅评分（BSS）
综合评分 0-100 分，来源于：
- 价格冲击（50% 权重）
- 成交量激增
- 恐慌指数峰值（30% 权重）
- 市值蒸发

评分等级：≥80（绿灯 - FTX 级重大事件），50-79（黄灯），<50（红灯）

### 4. 宏观股市熊市
综合评分来源于：
- VIX 恐慌指数（60% 权重）
- 股权风险溢价（40% 权重）：标普 500 股息率 - 10 年美债收益率

评分等级：≥0.8（绿灯 - 强烈宏观熊市），0.5-0.8（黄灯），<0.5（红灯）

### 5. 场外资金储备（SSR）
稳定币占加密总市值比例：
- 绿灯：SSR ≥ 10%（场外资金充裕，底部蓄势）
- 黄灯：SSR ≥ 7%（适度观望）
- 红灯：< 7%（资金在场内）

**重要**：高 SSR 表示大量资金逃离至稳定币（场外观望），这是熊市底部的典型特征，意味着有充足的"干火药"等待入场。

### 权重评分系统
系统使用加权评分进行更科学的判断：
- 黑天鹅强度：30%（最高权重，重大事件是底部关键信号）
- 市场极度恐慌：25%
- 场外资金储备：20%
- 矿工投降：15%
- 宏观股市熊市：10%

评分规则（绿灯=1.0，黄灯=0.5，红灯=0.0）：
- 加权评分 ≥70 分或 4-5 绿灯：强烈底部信号，建议建仓
- 加权评分 ≥55 分或 3 绿灯：底部特征显现，可关注
- 加权评分 <55 分：观望

## 依赖安装

```bash
pip install requests yfinance matplotlib numpy pandas
```

## 平台说明

- **macOS**：主要平台，使用 Launchd 进行调度（比 cron 更可靠，支持休眠/唤醒后补执行）
- **中文界面**：UI、日志和文档主要使用中文
- **字体配置**：matplotlib 使用 PingFang HK / Arial Unicode MS / SimHei 正确渲染中文
