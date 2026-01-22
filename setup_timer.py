import os
import plistlib
import subprocess
import sys

# =================配置区域=================
# 自动检测路径
PYTHON_PATH = sys.executable  # 自动使用当前 Python
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = os.path.join(SCRIPT_DIR, "crypto-bottom-tracker.py")
WORK_DIR = SCRIPT_DIR

# 任务名称 (类似 ID)
LABEL = "com.crypto.bottom-tracker"
# =========================================

def create_launch_agent():
    # 读取 .env 文件中的环境变量
    env_vars = {}
    env_file = os.path.join(WORK_DIR, '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()

    # 1. 定义 plist 内容 (Mac 任务描述文件)
    plist_content = {
        'Label': LABEL,
        'ProgramArguments': [PYTHON_PATH, SCRIPT_PATH],
        'WorkingDirectory': WORK_DIR,
        'EnvironmentVariables': env_vars,  # 添加环境变量
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
