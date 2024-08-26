# 文件: restore_vless.py

import os
import json
import subprocess

accounts_json = os.getenv('ACCOUNTS_JSON')
try:
    servers = json.loads(accounts_json)
except json.JSONDecodeError:
    error_message = "ACCOUNTS_JSON 参数格式错误"
    print(error_message)
    exit(1)

summary_message = "serv00-vless 恢复操作结果：\n"
default_restore_command = "cd ~/domains/$USER.serv00.net/vless && ./check_vless.sh"

for server in servers:
    host = server['host']
    port = server['port']
    username = server['username']
    password = server['password']
    cron_command = server.get('cron', default_restore_command)
    print(f"连接到 {host}...")
    restore_command = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no -p {port} {username}@{host} '{cron_command}'"
    try:
        output = subprocess.check_output(restore_command, shell=True, stderr=subprocess.STDOUT)
        summary_message += f"\n成功恢复 {host} 上的 vless 服务：\n{output.decode('utf-8')}"
    except subprocess.CalledProcessError as e:
        summary_message += f"\n无法恢复 {host} 上的 vless 服务：\n{e.output.decode('utf-8')}"

print(summary_message)
