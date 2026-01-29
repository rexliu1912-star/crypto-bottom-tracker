#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

# 如果数据文件不存在，先手动运行一次生成数据
if [ ! -f "web_data.json" ]; then
    echo "⚠️  未找到数据，正在生成..."
    python3 crypto-bottom-tracker.py
fi

echo "🚀 网页服务器已启动"
echo "👉 请打开: http://localhost:8000"
echo "⏹️  按 Ctrl+C 停止"
python3 -m http.server 8000
