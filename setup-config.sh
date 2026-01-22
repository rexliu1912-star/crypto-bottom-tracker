#!/bin/bash
# Crypto Bottom Tracker - 交互式配置脚本

clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🔧 Crypto Bottom Tracker - 配置向导"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查是否已存在 .env 文件
if [ -f .env ]; then
    echo "⚠️  检测到已存在的 .env 文件"
    read -p "是否覆盖现有配置？(y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "✅ 保留现有配置，退出向导"
        exit 0
    fi
    echo "📝 将覆盖现有配置..."
    echo ""
fi

# 创建 .env 文件
echo "📝 开始配置 API 密钥..."
echo ""

# 1. Telegram Bot Token
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  Telegram Bot Token"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 请先完成以下步骤："
echo "   1. 打开 Telegram 找到 @BotFather"
echo "   2. 发送 /mybots 选择你的 Bot"
echo "   3. 点击 'API Token'"
echo "   4. 如果是旧 Token，先 'Revoke current token'"
echo "   5. 点击 'Generate new token' 生成新 Token"
echo ""
echo "格式示例: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
echo ""
read -p "请输入 Telegram Bot Token: " BOT_TOKEN

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ Token 不能为空，配置失败"
    exit 1
fi

# 2. Telegram Chat ID
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  Telegram Chat ID"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 获取 Chat ID："
echo "   1. 打开 Telegram 找到 @userinfobot"
echo "   2. 发送任意消息"
echo "   3. Bot 会返回你的 Chat ID"
echo ""
echo "格式示例: -1001234567890 或 123456789"
echo ""
read -p "请输入 Telegram Chat ID: " CHAT_ID

if [ -z "$CHAT_ID" ]; then
    echo "❌ Chat ID 不能为空，配置失败"
    exit 1
fi

# 3. Polygon API Key (可选)
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  Polygon.io API Key (可选)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "用于获取 VIX 数据（宏观指标）"
echo "如果没有，程序会使用 yfinance 备用方案"
echo ""
read -p "请输入 Polygon API Key (直接按 Enter 跳过): " POLYGON_KEY

# 写入 .env 文件
cat > .env << EOF
# Crypto Bottom Tracker - 环境变量配置
# 生成时间: $(date)

# Telegram Bot 配置
TELEGRAM_BOT_TOKEN=$BOT_TOKEN
TELEGRAM_CHAT_ID=$CHAT_ID

# Polygon.io API 配置（可选）
POLYGON_API_KEY=$POLYGON_KEY
EOF

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 配置完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📄 配置文件已保存到: .env"
echo ""
echo "🔒 安全提醒："
echo "   - .env 文件不会被提交到 Git"
echo "   - 请勿分享 .env 文件给他人"
echo "   - 定期更新 API 密钥以保证安全"
echo ""
echo "🚀 下一步："
echo "   运行程序: ./run.sh"
echo "   或: python3 crypto-bottom-tracker.py"
echo ""

# 询问是否立即测试
read -p "是否立即测试运行程序？(Y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo ""
    echo "🧪 开始测试..."
    ./run.sh
fi
