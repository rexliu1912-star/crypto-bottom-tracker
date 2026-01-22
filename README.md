# 📉📈 Crypto Bottom Tracker / 加密底部追踪器

> A Python tool for tracking and identifying potential market bottoms in cryptocurrency markets.

**English** | [中文](#中文说明)

## Overview

This tool monitors **five key indicators** to identify potential market bottoms:
- Market Sentiment (Fear & Greed Index)
- Miner Capitulation (Price Drawdown)
- Black Swan Events (Crisis Score)
- Macro Environment (VIX + ERP)
- Off-Exchange Liquidity (Stablecoin Ratio)

**Features:**
- ✅ Real-time data from multiple APIs
- ✅ Weighted scoring system (0-100)
- ✅ Web dashboard with auto-refresh
- ✅ Telegram notifications
- ✅ Smart caching (6-24 hours)

**System Reliability:** ⭐⭐⭐⭐ (4/5)

---

## 中文说明

一个用于跟踪并识别加密货币市场潜在底部的 Python 工具。通过五大指标（市场情绪、矿工投降、黑天鹅、宏观环境、流动性）输出**红/黄/绿灯仪表盘**，并自动生成可视化图表。

仪表盘居中显示"加密底部追踪器"标题，下方显示当前时间，五个指标以正圆形指示灯呈现。

## 📸 截图预览

![仪表盘截图](dashboard.png)

## @Tinghu888 推特原文

https://x.com/TingHu888/status/1602192185109057536 (2022-12-12: 强调综合看现状，避免单指标判断熊市) 

https://x.com/TingHu888/status/1595025672254230531 (2022-11-22: 提到黑天鹅已来，判断大熊市非量化指标) 

https://x.com/TingHu888/status/1580073905603063809 (2022-10-12: 明确熊市底部有黑天鹅事件，作为进场信号) 

https://x.com/TingHu888/status/1524317641892335617 (2022-05-11: 讨论情绪指标在熊市中的有效性) 

https://x.com/TingHu888/status/1514197274728882179 (2022-04-13: 强调熊市看流动性逃离/总市值，牛市看流动性涌入) 

## 🚀 功能亮点

- ✅ 自动抓取实时数据
- ✅ 五大底部指标判定
- ✅ 自动输出熊市底部仪表盘 PNG
- ✅ 稳定断网 fallback
- ✅ 分析底部强弱的灯号系统
- ✅ **Telegram 推送**（支持文字和图片）
- ✅ **网页展示界面**（实时查看指标，美观的深色主题）
- ✅ **Polygon.io API 集成**（永不限流的宏观数据源）
- ✅ **混合数据源方案**（Polygon + yfinance 自动切换）
- ✅ **智能缓存机制**（6小时缓存，避免 API 限流）

## 📦 安装

```bash
pip install requests yfinance matplotlib numpy pandas
```

## 🔑 API 配置

程序使用以下 API：

- **Telegram Bot API**：用于推送消息和图片
- **Polygon.io API**：用于获取宏观股市数据（VIX、TNX），永不限流
- **yfinance**：备用数据源（当 Polygon API 不可用时，带6小时缓存）
- **CoinGecko API**：免费获取加密货币数据
- **Blockchain.info API**：获取比特币哈希率数据

### 配置步骤

**方法 1：使用环境变量（推荐）**

1. 复制配置模板：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填入你的 API 密钥：
   ```bash
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   POLYGON_API_KEY=your_polygon_key_here  # 可选
   ```

3. 运行前加载环境变量：
   ```bash
   # macOS/Linux
   export $(cat .env | xargs)
   python3 crypto-bottom-tracker.py

   # 或使用 source
   source .env
   python3 crypto-bottom-tracker.py
   ```

**方法 2：系统环境变量**

在 `~/.zshrc` 或 `~/.bashrc` 中添加：
```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
export POLYGON_API_KEY="your_key_here"
```

**获取 API 密钥：**
- `TELEGRAM_BOT_TOKEN`：从 [@BotFather](https://t.me/BotFather) 获取
- `TELEGRAM_CHAT_ID`：从 [@userinfobot](https://t.me/userinfobot) 获取
- `POLYGON_API_KEY`：从 [polygon.io](https://polygon.io) 获取（可选）

## ▶️ 运行

### 手动执行

```bash
# 立即执行一次
python3 crypto-bottom-tracker.py
```

### 定时任务设置（推荐）

使用 macOS Launchd 实现每日自动推送（比 cron 更可靠，支持休眠唤醒后补执行）：

```bash
# 一键设置每日 08:00 自动执行
python3 setup_timer.py
```

设置成功后可使用以下命令：

```bash
# 查看任务状态
launchctl list | grep com.crypto.bottom-tracker

# 手动立即执行
launchctl start com.crypto.bottom-tracker

# 停止/卸载任务
launchctl unload ~/Library/LaunchAgents/com.crypto.bottom-tracker.plist
```

### 执行流程

程序执行时会：
1. 获取市场数据（恐惧贪婪指数、哈希率、黑天鹅评分等）
2. 计算五大指标
3. 生成仪表盘图片（保存到桌面）
4. 生成网页数据文件（`web_data.json`）
5. 推送到 Telegram（文字报告 + 图片）

## 🌐 网页展示

程序支持网页展示功能，可以在浏览器中实时查看指标状态。

### 启动网页

```bash
# 方式一：使用启动脚本
./启动网页.sh

# 方式二：直接打开 HTML 文件
open index.html

# 方式三：使用 Python 服务器
python3 -m http.server 8000
# 然后在浏览器中打开 http://localhost:8000
```

### 网页功能

- ✅ 实时展示五大指标状态
- ✅ 颜色标识（绿灯/黄灯/红灯）
- ✅ 自动刷新（每 30 秒）
- ✅ 响应式设计（支持手机和电脑）
- ✅ 美观的深色主题界面

详细说明请查看：`网页使用说明.md`

## 🧠 五大指标解释

### 1. 市场极度恐慌（FGI）

| 灯号 | 条件      | 说明                   |
|------|-----------|------------------------|
| 🟩   | FGI ≤ 20  | 极度恐慌，底部特征强烈 |
| 🟨   | FGI ≤ 35  | 偏恐慌                 |
| 🟥   | > 35      | 情绪正常或偏乐观       |

### 2. 矿工投降（哈希率变化）

| 灯号 | 条件     | 说明           |
|------|----------|----------------|
| 🟩   | < -18%   | 强投降，底部常见 |
| 🟨   | < -5%    | 轻度投降       |
| 🟥   | ≥ -5%    | 稳定或上涨     |

### 3. 黑天鹅强度 (BSS - Black Swan Score)

| 灯号 | 条件       | 说明                                           |
|------|------------|------------------------------------------------|
| 🟩   | BSS ≥ 80   | 强烈黑天鹅（2022.11 FTX、2018.11、2020.3 级别）|
| 🟨   | BSS 50~79  | 有一定冲击，需关注                             |
| 🟥   | BSS < 50   | 正常波动                                       |

**BSS 评分系统**：综合评估价格冲击、交易量激增、恐慌峰值、市值蒸发四个维度，加权计算得出 0-100 分的黑天鹅强度评分。

### 4. 宏观股市熊市（VIX + ERP）

| 灯号 | 条件              | 说明                           |
|------|-------------------|--------------------------------|
| 🟩   | 综合评分 ≥ 0.8    | 强烈宏观熊市信号（VIX>35 或 ERP>5%）|
| 🟨   | 综合评分 0.5~0.8  | 宏观风险上升（VIX>25 或 ERP>3%）|
| 🟥   | 综合评分 < 0.5    | 宏观环境正常                   |

**评分系统**：
- VIX 恐慌指数（权重 60%）：衡量市场恐慌情绪
- ERP 股权风险溢价（权重 40%）：S&P500 股息率 - 10年美债收益率
- 数据源：优先使用 Polygon.io API，失败时回退到 yfinance（带缓存）

### 5. 场外资金储备（SSR）

| 灯号 | 条件      | 说明               |
|------|-----------|--------------------|
| 🟩   | SSR ≥ 10% | 场外资金充裕，底部蓄势 |
| 🟨   | SSR ≥ 7%  | 适度观望，资金在场外 |
| 🟥   | < 7%      | 资金在场内           |

**说明**：高 SSR 表示大量资金逃离至稳定币（场外观望），这是熊市底部的典型特征，意味着有充足的"干火药"等待入场。

## 🎯 最终判断（权重评分系统 + 绿灯数量）

### 权重分配

| 指标 | 权重 | 说明 |
|------|------|------|
| 黑天鹅强度 | 30% | 最高权重，重大事件是底部关键信号 |
| 市场极度恐慌 | 25% | 情绪指标，反映市场恐慌程度 |
| 场外资金储备 | 20% | 流动性指标，衡量潜在买盘 |
| 矿工投降 | 15% | 成本压力，矿工投降标志底部 |
| 宏观股市熊市 | 10% | 宏观环境，影响资金流向 |

### 综合判断

| 加权评分 | 绿灯数量 | 市场状态           |
|----------|----------|--------------------|
| ≥70 分或 4-5 个 | - | 📈 强烈底部信号，建议建仓 |
| ≥55 分或 3 个 | - | 🔍 底部特征显现，可关注 |
| <55 分 | 0-2 | 🐻 观望 |

**说明**：系统综合考虑权重评分和绿灯数量，黑天鹅事件因其在底部判断中的关键作用获得最高权重。

## 🖼 输出

- 指标与灯号列表（控制台输出）
- `dashboard.png`（保存到项目目录）

### 仪表盘特性

- **标题**：居中显示"加密底部追踪器"
- **时间戳**：标题下方显示当前时间（格式：YYYY-MM-DD HH:MM:SS）
- **指标显示**：五个指标以正圆形指示灯显示（🟩绿灯/🟨黄灯/🟥红灯）
- **数据详情**：每个指标显示具体数值和变化趋势

## 🔧 故障排查

### Telegram 推送失败

1. 检查配置：确认 `TELEGRAM_BOT_TOKEN` 和 `TELEGRAM_CHAT_ID` 已正确配置
2. 测试连接：运行 `python3 crypto-bottom-tracker.py`
3. 确认权限：确保已向机器人发送过 `/start`

### 数据获取失败

- 程序有完善的降级机制，会自动切换数据源
- yfinance 数据使用6小时缓存，避免频繁请求
- 如果所有数据源都失败，会使用默认值继续执行

### 图片生成失败

- 检查当前目录是否有写入权限
- 图片会保存到项目目录：`dashboard.png`

## 📝 更新日志

### 2026-01-22 (重大更新)
- ✅ **修复五大指标真实数据获取**
  - 实现矿工投降指标（BTC 价格回撤作为矿工压力代理）
  - 实现场外资金储备指标（真实 SSR 数据）
  - 为两个指标添加 6 小时智能缓存
- ✅ **优化 SSR 指标逻辑**
  - 修正指标名称："流动性恢复" → "场外资金储备"
  - 优化阈值：≥10%（绿灯），≥7%（黄灯），<7%（红灯）
  - 符合 TingHu888 理论：高 SSR = 场外资金充裕（底部蓄势）
- ✅ **增加权重评分系统**
  - 黑天鹅强度 30%（最高权重）
  - 市场极度恐慌 25%
  - 场外资金储备 20%
  - 矿工投降 15%
  - 宏观股市熊市 10%
  - 权重评分 ≥70 分或 4-5 绿灯 → 建议建仓
- ✅ **完成系统评估与回测**
  - 创建《系统评估与回测.md》文档
  - 验证系统能成功捕捉 2022 年底部（FTX 崩盘）
  - 总体评分 4/5 星

### 2026-01-11
- ✅ 清理项目结构，统一文件命名
- ✅ 添加 README 截图预览
- ✅ 优化定时任务配置

### 2025-12-12
- ✅ 移除自动推送功能，简化为手动执行模式
- ✅ 保留所有核心功能
- ✅ 优化代码结构

### 2025-12-11
- ✅ 集成 Polygon.io API（永不限流）
- ✅ 实现混合数据源方案（Polygon 优先，yfinance 备用）
- ✅ 添加智能缓存机制（6小时缓存）
- ✅ 改进评分算法（VIX 权重 60%，ERP 权重 40%）
