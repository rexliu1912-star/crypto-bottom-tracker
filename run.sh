#!/bin/bash
# Crypto Bottom Tracker - 启动脚本

echo "🚀 启动加密底部追踪器..."

# 检查 .env 文件是否存在
if [ ! -f .env ]; then
    echo "❌ 错误：找不到 .env 配置文件"
    echo ""
    echo "请先运行配置脚本："
    echo "  ./setup-config.sh"
    echo ""
    echo "或手动创建 .env 文件："
    echo "  cp .env.example .env"
    echo "  nano .env  # 然后填入你的 API 密钥"
    exit 1
fi

# 检查 .env 中是否配置了 Token
if grep -q "请在这里填入新的Bot Token" .env; then
    echo "⚠️  警告：检测到 .env 文件未配置"
    echo ""
    echo "请编辑 .env 文件，填入你的真实 API 密钥："
    echo "  nano .env"
    echo ""
    read -p "按 Enter 继续编辑，或 Ctrl+C 取消..."
    nano .env
fi

# 加载环境变量
echo "📝 加载环境变量..."
export $(cat .env | grep -v '^#' | xargs)

# 检查必要的环境变量
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ 错误：TELEGRAM_BOT_TOKEN 未设置"
    exit 1
fi

if [ -z "$TELEGRAM_CHAT_ID" ]; then
    echo "❌ 错误：TELEGRAM_CHAT_ID 未设置"
    exit 1
fi

echo "✅ 配置已加载"
echo ""

# 运行程序
echo "▶️  运行程序..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 crypto-bottom-tracker.py
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ 运行完成！"
