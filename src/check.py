from flask import Flask, request, jsonify
import json
import requests
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'data.json'
DISCORD_WEBHOOK = 'https://discord.com/api/webhooks/1379092851912343663/jelBiRmYvSqfRByzWa5_ppUzoxvsU8VXIauKfRqBirkjKFjMzXWQNNM67JldrtOkDirf'

def load_whitelist():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f).get('whitelist', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_whitelist(whitelist):
    with open(DATA_FILE, 'w') as f:
        json.dump({'whitelist': whitelist}, f)

def send_discord_webhook(data):
    embed = {
        "title": "玩家验证通知",
        "color": 0x3498db,
        "fields": [
            {"name": "用户名", "value": data.get('username', 'N/A'), "inline": True},
            {"name": "UserID", "value": str(data.get('userid', 'N/A')), "inline": True},
            {"name": "HWID", "value": data.get('hwid', 'N/A'), "inline": False},
            {"name": "IP地址", "value": data.get('ip', 'N/A'), "inline": True},
            {"name": "验证结果", "value": "成功" if data.get('whitelisted') else "失败", "inline": True},
            {"name": "时间", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "inline": False}
        ]
    }
    payload = {"embeds": [embed]}
    requests.post(DISCORD_WEBHOOK, json=payload)

@app.route('/verify', methods=['POST'])
def verify_player():
    try:
        player_data = request.get_json()
        username = player_data.get('username', '')
        hwid = player_data.get('hwid', '')
        userid = player_data.get('userid', '')
        ip = player_data.get('ip', '')

        whitelist = load_whitelist()
        is_whitelisted = username in whitelist

        webhook_data = {
            'username': username,
            'hwid': hwid,
            'userid': userid,
            'ip': ip,
            'whitelisted': is_whitelisted
        }
        send_discord_webhook(webhook_data)

        if is_whitelisted:
            return "By Moxiaobai Content:True\nscriptid: Moxiaobai", 200
        else:
            return "By Moxiaobai Content:False\nscriptid: Moxiaobai", 403
            
    except Exception as e:
        return f"错误: {str(e)}\nscriptid: Moxiaobai", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
