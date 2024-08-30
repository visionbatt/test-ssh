import os
import json
import paramiko

# 获取环境变量中的账户信息
accounts_json = os.getenv('ACCOUNTS_JSON')

# 尝试加载 JSON 数据
try:
    servers = json.loads(accounts_json)
except json.JSONDecodeError:
    print("ACCOUNTS_JSON 参数格式错误")
    exit(1)

summary_message = "serv00-vless 恢复操作结果：\n"
default_restore_command = "cd ~/domains/$USER.serv00.net/vless && ./check_vless.sh"

# 遍历每个服务器信息
for server in servers:
    host = server['host']
    port = server['port']
    username = server['username']
    password = server['password']
    cron_command = server.get('cron', default_restore_command)

    print(f"连接到 {host}...")
    
    # 使用 Paramiko 进行 SSH 连接
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动添加主机密钥

    try:
        ssh.connect(hostname=host, port=port, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(cron_command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if output:
            summary_message += f"\n成功恢复 {host} 上的 vless 服务：\n{output}"
        if error:
            summary_message += f"\n恢复 {host} 上的 vless 服务时出错：\n{error}"
    except paramiko.SSHException as e:
        summary_message += f"\n无法恢复 {host} 上的 vless 服务：\n{str(e)}"
    finally:
        ssh.close()

print(summary_message)
