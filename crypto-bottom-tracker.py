# ===== 加密熊市底部追踪器 · 纯净执行版 (v4.0) =====
import requests, matplotlib, matplotlib.pyplot as plt, numpy as np, os, getpass, time, warnings, json, platform
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
warnings.filterwarnings('ignore')

# --- .env 自动加载 ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv 未安装时跳过

# --- 配置区 ---
# 从环境变量读取 API 密钥（更安全的方式）
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "")

# 全局 FGI 缓存（避免重复请求）
_cached_fgi = None

# CoinGecko 全局限流
_last_coingecko_call = 0
def _coingecko_throttle():
    """确保 CoinGecko 请求间隔至少 3 秒"""
    global _last_coingecko_call
    elapsed = time.time() - _last_coingecko_call
    if elapsed < 3:
        time.sleep(3 - elapsed)
    _last_coingecko_call = time.time()

# --- 绘图设置 ---
# 跨平台中文字体支持
if platform.system() == 'Darwin':
    plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Arial Unicode MS', 'SimHei']
elif platform.system() == 'Linux':
    plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'DejaVu Sans']
else:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('dark_background')

# --- 基础函数 ---
def send_telegram_message(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
        requests.post(url, data=data, timeout=10)
    except Exception as e: print(f"消息发送失败: {e}")

def send_telegram_photo(photo_path):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        with open(photo_path, 'rb') as photo:
            requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID}, files={'photo': photo}, timeout=30)
    except Exception as e: print(f"图片发送失败: {e}")

def get_black_swan_status():
    """获取黑天鹅评分，带 12 小时缓存"""
    cache_file = ".bss_cache.txt"
    cache_duration = 12 * 3600  # 12小时

    # 检查缓存
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 3:
                    cache_time = float(lines[0].strip())
                    cached_status = lines[1].strip()
                    cached_bss = float(lines[2].strip())
                    if time.time() - cache_time < cache_duration:
                        print(f"使用缓存的黑天鹅数据: {cached_status}, BSS={cached_bss:.1f}")
                        return cached_status, cached_bss
        except:
            pass

    # 获取新数据
    try:
        _coingecko_throttle()
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=180&interval=daily"
        data = requests.get(url, timeout=12).json()
        df = pd.DataFrame(data['prices'], columns=['ts', 'price'])
        df['date'] = pd.to_datetime(df['ts'], unit='ms').dt.date
        df['volume'] = [v[1] for v in data['total_volumes']]

        # 计算 BSS (简化版)
        price_chg = -(df['price'].iloc[-1] - df['price'].iloc[0]) / df['price'].iloc[0]
        price_score = max(0, price_chg * 250)
        # 成交量激增评分：最近7天均量 vs 180天均量
        recent_vol = df['volume'].iloc[-7:].mean()
        avg_vol = df['volume'].mean()
        vol_ratio = recent_vol / avg_vol if avg_vol > 0 else 1.0
        vol_score = min(100, max(0, (vol_ratio - 1.0) * 100))  # 超出均值部分转为分数

        # 恐慌指数评分（使用缓存的 FGI，避免重复请求）
        fg = _cached_fgi if _cached_fgi is not None else 40
        fear_score = max(0, (45 - fg) * 3.0)

        bss = min(100, price_score * 0.5 + fear_score * 0.3 + vol_score * 0.2)  # 价格50% + 恐慌30% + 成交量20%

        if bss >= 80:
            status = "绿灯"
        elif bss >= 50:
            status = "黄灯"
        else:
            status = "红灯"

        # 写入缓存
        try:
            with open(cache_file, 'w') as f:
                f.write(f"{time.time()}\n")
                f.write(f"{status}\n")
                f.write(f"{bss}\n")
        except:
            pass

        return status, bss
    except:
        return "红灯", 20.0

def get_polygon_aggs(symbol):
    try:
        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{from_date}/{to_date}?limit=10&apiKey={POLYGON_API_KEY}"
        res = requests.get(url, timeout=5).json()
        if 'results' in res: return res['results'][-1]['c']
    except: pass
    return None

def get_vix_with_fallback():
    """获取 VIX 数据，Polygon 失败时使用 yfinance 备用"""
    cache_file = ".vix_cache.txt"
    cache_duration = 6 * 3600  # 6小时

    # 检查缓存
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    cache_time = float(lines[0].strip())
                    cached_vix = float(lines[1].strip())
                    if time.time() - cache_time < cache_duration:
                        print(f"使用缓存的 VIX 数据: {cached_vix:.1f}")
                        return cached_vix
        except:
            pass

    # 方案1: Polygon.io API
    vix = get_polygon_aggs("VIX")
    if vix is not None:
        # 写入缓存
        try:
            with open(cache_file, 'w') as f:
                f.write(f"{time.time()}\n{vix}\n")
        except:
            pass
        return vix

    # 方案2: yfinance 备用
    try:
        print("Polygon API 无数据，使用 yfinance 备用方案")
        vix_ticker = yf.Ticker("^VIX")
        hist = vix_ticker.history(period="5d")
        if not hist.empty:
            vix = hist['Close'].iloc[-1]
            # 写入缓存
            try:
                with open(cache_file, 'w') as f:
                    f.write(f"{time.time()}\n{vix}\n")
            except:
                pass
            return vix
    except Exception as e:
        print(f"yfinance 获取 VIX 失败: {e}")

    # 方案3: 默认值
    print("使用默认 VIX 值: 20.0")
    return 20.0

def get_hashrate_data():
    """获取比特币价格数据作为矿工压力代理指标，带 6 小时缓存"""
    cache_file = ".miner_cache.txt"
    cache_duration = 6 * 3600  # 6 小时

    # 检查缓存
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 3:
                    cache_time = float(lines[0].strip())
                    cached_price = float(lines[1].strip())
                    cached_drawdown = float(lines[2].strip())
                    if time.time() - cache_time < cache_duration:
                        print(f"使用缓存的矿工投降数据: ${cached_price:,.0f}, 回撤 {cached_drawdown:.1f}%")
                        return cached_price, cached_drawdown
        except:
            pass

    try:
        _coingecko_throttle()

        # 使用 CoinGecko 获取 BTC 30 天价格数据
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30&interval=daily"
        response = requests.get(url, timeout=10)

        if response.status_code == 429:
            print("CoinGecko API 速率限制，矿工投降使用默认值")
            return None, None

        data = response.json()

        if 'prices' in data and len(data['prices']) >= 2:
            prices = data['prices']
            current_price = prices[-1][1]  # 最新价格
            old_price = prices[0][1]  # 30天前价格

            # 找到最高价格
            max_price = max([p[1] for p in prices])

            # 计算从高点的回撤（作为矿工压力的代理指标）
            drawdown = ((current_price - max_price) / max_price) * 100

            # 写入缓存
            try:
                with open(cache_file, 'w') as f:
                    f.write(f"{time.time()}\n")
                    f.write(f"{current_price}\n")
                    f.write(f"{drawdown}\n")
            except:
                pass

            return current_price, drawdown
    except Exception as e:
        print(f"矿工投降指标数据获取失败: {e}")

    return None, None

def get_stablecoin_dominance():
    """获取稳定币占比 (SSR)，带 24 小时缓存"""
    cache_file = ".ssr_cache.txt"
    cache_duration = 24 * 3600  # 24 小时（SSR 变化不频繁）

    # 检查缓存
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    cache_time = float(lines[0].strip())
                    cached_ssr = float(lines[1].strip())
                    if time.time() - cache_time < cache_duration:
                        print(f"使用缓存的 SSR 数据: {cached_ssr:.1f}%")
                        return cached_ssr
        except:
            pass

    try:
        _coingecko_throttle()

        # 获取稳定币总市值（USDT + USDC + DAI）
        stablecoin_ids = "tether,usd-coin,dai"
        url1 = f"https://api.coingecko.com/api/v3/simple/price?ids={stablecoin_ids}&vs_currencies=usd&include_market_cap=true"
        stable_response = requests.get(url1, timeout=10)

        if stable_response.status_code == 429:
            print("CoinGecko API 速率限制，使用默认 SSR 值")
            return None

        stable_data = stable_response.json()

        # 计算稳定币总市值
        stable_mcap = sum([
            stable_data.get('tether', {}).get('usd_market_cap', 0),
            stable_data.get('usd-coin', {}).get('usd_market_cap', 0),
            stable_data.get('dai', {}).get('usd_market_cap', 0)
        ])

        # 获取加密总市值
        _coingecko_throttle()
        url2 = "https://api.coingecko.com/api/v3/global"
        global_response = requests.get(url2, timeout=10)

        if global_response.status_code == 429:
            print("CoinGecko API 速率限制，使用默认 SSR 值")
            return None

        global_data = global_response.json()

        if 'data' in global_data and 'total_market_cap' in global_data['data']:
            total_mcap = global_data['data']['total_market_cap'].get('usd', 0)

            if total_mcap > 0:
                ssr = (stable_mcap / total_mcap) * 100

                # 写入缓存
                try:
                    with open(cache_file, 'w') as f:
                        f.write(f"{time.time()}\n")
                        f.write(f"{ssr}\n")
                except:
                    pass

                return ssr
    except Exception as e:
        print(f"稳定币占比数据获取失败: {e}")

    return None

def run_tracker():
    print(f"Executing Tracker: {datetime.now()}")
    
    # 1. 获取数据
    status_data = []
    
    # (FGI) - 先获取并缓存，供 BSS 复用
    global _cached_fgi
    try:
        fg_data = requests.get("https://api.alternative.me/fng/?limit=2", timeout=8).json()['data']
        fg_curr = int(fg_data[0]['value'])
        fg_chg = fg_curr - int(fg_data[1]['value'])
        _cached_fgi = fg_curr
    except: fg_curr, fg_chg = 30, 0; _cached_fgi = 30
    
    f_stat = "green" if fg_curr <= 20 else ("yellow" if fg_curr <= 35 else "red")
    status_data.append({
        "name": "市场极度恐慌", "status": f_stat,
        "fullText": f"{'🟢' if f_stat=='green' else '🟡' if f_stat=='yellow' else '🔴'} (当前:{fg_curr}, 变化:{fg_chg:+d})"
    })

    # (Hashrate) - 使用价格回撤作为矿工压力代理指标
    btc_price, drawdown = get_hashrate_data()
    if btc_price is not None and drawdown is not None:
        # 价格回撤阈值：<-30%（强压力/绿灯），<-15%（中等压力/黄灯），>-15%（红灯）
        h_stat = "green" if drawdown < -30 else ("yellow" if drawdown < -15 else "red")
        status_data.append({
            "name": "矿工投降", "status": h_stat,
            "fullText": f"{'🟢' if h_stat=='green' else '🟡' if h_stat=='yellow' else '🔴'} (回撤:{drawdown:.1f}%, 价格:${btc_price:,.0f})"
        })
    else:
        # 降级方案：使用默认值
        status_data.append({
            "name": "矿工投降", "status": "yellow",
            "fullText": "🟡 (数据获取失败，使用默认值)"
        })

    # (Black Swan)
    bs_str, bs_val = get_black_swan_status()
    b_stat = "green" if bs_str=="绿灯" else "yellow" if bs_str=="黄灯" else "red"
    status_data.append({
        "name": "黑天鹅强度", "status": b_stat,
        "fullText": f"{'🟢' if b_stat=='green' else '🟡' if b_stat=='yellow' else '🔴'} (BSS:{bs_val:.1f})"
    })

    # (Macro) - 使用备用方案获取 VIX
    vix = get_vix_with_fallback()
    # TODO: 实现真实 ERP 计算（S&P500 earnings yield - 10Y Treasury yield）
    # 当前仅使用 VIX 作为宏观熊市指标
    m_stat = "green" if vix > 35 else "yellow" if vix > 25 else "red"
    status_data.append({
        "name": "宏观股市熊市", "status": m_stat,
        "fullText": f"{'🟢' if m_stat=='green' else '🟡' if m_stat=='yellow' else '🔴'} (VIX:{vix:.1f})"
    })

    # (SSR) - 真实稳定币占比数据
    # 修正逻辑：SSR 高表示大量场外资金（底部蓄势特征）
    ssr = get_stablecoin_dominance()
    if ssr is not None:
        # 优化阈值：>10% 强烈底部信号，7-10% 底部特征，<7% 资金在场内
        ssr_stat = "green" if ssr >= 10 else ("yellow" if ssr >= 7 else "red")
        ssr_desc = "场外充裕" if ssr >= 10 else "适度观望" if ssr >= 7 else "资金在场"
        status_data.append({
            "name": "场外资金储备", "status": ssr_stat,
            "fullText": f"{'🟢' if ssr_stat=='green' else '🟡' if ssr_stat=='yellow' else '🔴'} (SSR:{ssr:.1f}%, {ssr_desc})"
        })
    else:
        # 降级方案：使用默认值
        status_data.append({
            "name": "场外资金储备", "status": "yellow",
            "fullText": "🟡 (数据获取失败，使用默认值)"
        })

    # 统计 - 基础绿灯数量
    green_count = sum(1 for s in status_data if s['status'] == 'green')

    # 增加权重评分系统（更科学的判断）
    weights = {
        "市场极度恐慌": 0.25,
        "矿工投降": 0.15,
        "黑天鹅强度": 0.30,  # 最高权重
        "宏观股市熊市": 0.10,
        "场外资金储备": 0.20
    }

    # 计算加权评分（绿=1.0, 黄=0.5, 红=0.0）
    score_map = {"green": 1.0, "yellow": 0.5, "red": 0.0}
    weighted_score = sum(
        weights[ind["name"]] * score_map[ind["status"]]
        for ind in status_data
    )

    # 综合判断（权重优先，绿灯数量作为参考）
    if weighted_score >= 0.70 or green_count >= 4:
        mkt_status = "强烈底部信号，建议建仓"
        mkt_type = "buy"
    elif weighted_score >= 0.55 or green_count == 3:
        mkt_status = "底部特征显现，可关注"
        mkt_type = "watch"
    else:
        mkt_status = "观望"
        mkt_type = "wait"

    # 生成 Web JSON
    web_json = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "indicators": [{"name":i['name'], "status":i['status'], "statusText":"-", "data":i['fullText'], "fullText":i['fullText']} for i in status_data],
        "greenCount": green_count,
        "totalCount": 5,
        "weightedScore": round(weighted_score * 100, 1),  # 转换为百分比
        "marketStatus": mkt_status,
        "marketStatusType": mkt_type
    }
    with open("web_data.json", "w", encoding='utf-8') as f:
        json.dump(web_json, f, ensure_ascii=False)

    # 绘图
    try:
        USER = getpass.getuser()
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.axis('off')
        ax.text(0.5, 0.8, "加密底部追踪器", ha='center', color='white', fontsize=30, weight='bold')
        ax.text(0.5, 0.73, datetime.now().strftime('%Y-%m-%d'), ha='center', color='gray', fontsize=15)
        
        for i, item in enumerate(status_data):
            y = 0.6 - i * 0.12
            col = {'green':'limegreen','yellow':'orange','red':'crimson'}[item['status']]
            ax.add_patch(plt.Circle((0.2, y), 0.03, color=col))
            ax.text(0.3, y, item['name'], ha='left', va='center', color='white', fontsize=16)
            # 安全解析括号内的数据文字
            try:
                detail_text = item['fullText'].split('(')[1].rstrip(')')
            except (IndexError, AttributeError):
                detail_text = item['fullText']
            ax.text(0.7, y, detail_text, ha='left', va='center', color='gray', fontsize=14)
            
        # 保存到项目目录，避免桌面权限问题
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, "dashboard.png")
        plt.savefig(path, dpi=200, facecolor='black')
        plt.close()
        
        # 推送
        report = f"🐻 <b>加密追踪</b>\n绿灯: {green_count}/5\n状态: {mkt_status}"
        send_telegram_message(report)
        send_telegram_photo(path)
        print("✅ 执行完成")
    except Exception as e:
        print(f"❌ 绘图/推送错误: {e}")

if __name__ == "__main__":
    run_tracker()
