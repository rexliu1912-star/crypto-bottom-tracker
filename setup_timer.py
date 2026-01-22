import os
import plistlib
import subprocess

# =================配置区域=================
# 您的 Python 路径
PYTHON_PATH = "/Library/Frameworks/Python.framework/Versions/3.14/bin/python3"
# 您的脚本路径
SCRIPT_PATH = "/Users/rexliu1912/vibe-coding/crypto-bottom-tracker/crypto-bottom-tracker.py"
# 工作目录 (脚本所在的文件夹)
WORK_DIR = "/Users/rexliu1912/vibe-coding/crypto-bottom-tracker/"

# 任务名称 (类似 ID)
LABEL = "com.crypto.bottom-tracker"
# =========================================

def create_launch_agent():
    # 1. 定义 plist 内容 (Mac 任务描述文件)
    plist_content = {
        'Label': LABEL,
        'ProgramArguments': [PYTHON_PATH, SCRIPT_PATH],
        'WorkingDirectory': WORK_DIR,
        'StartCalendarInterval': {
            'Hour': 8,     # 每天早上 8 点
            'Minute': 0    # 0 分
        },
        'StandardOutPath': os.path.join(WORK_DIR, 'tracker.log'),
        'StandardErrorPath': os.path.join(WORK_DIR, 'tracker.log'),
        'RunAtLoad': False
    }

    # 2. 确定保存路径: ~/Library/LaunchAgents/
    home_dir = os.path.expanduser("~")
    agent_dir = os.path.join(home_dir, "Library", "LaunchAgents")
    if not os.path.exists(agent_dir):
        os.makedirs(agent_dir)
    
    plist_path = os.path.join(agent_dir, f"{LABEL}.plist")

    # 3. 写入文件
    with open(plist_path, 'wb') as f:
        plistlib.dump(plist_content, f)
    
    print(f"✅ 配置文件已生成: {plist_path}")

    # 4. 激活任务
    # 先卸载旧的(如果有)，防止重复
    unload_cmd = f"launchctl unload {plist_path}"
    subprocess.run(unload_cmd, shell=True, stderr=subprocess.DEVNULL)
    
    # 加载新的
    load_cmd = f"launchctl load {plist_path}"
    result = subprocess.run(load_cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("🎉 成功！定时任务已启动。")
        print("📅 每天早上 08:00 将自动运行脚本。")
        print(f"📄 运行日志将保存在: {os.path.join(WORK_DIR, 'tracker.log')}")
        print("")
        print("📋 常用命令:")
        print(f"   查看状态: launchctl list | grep {LABEL}")
        print(f"   立即执行: launchctl start {LABEL}")
        print(f"   停止任务: launchctl unload {plist_path}")
    else:
        print("❌ 启动失败，请检查报错信息：")
        print(result.stderr)

if __name__ == "__main__":
    create_launch_agent()
