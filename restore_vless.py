import os
import json
import paramiko

# 从环境变量中获取 ACCOUNTS_JSON
accounts_json = os.getenv('ACCOUNTS_JSON')

try:
    servers = json.loads(accounts_json)
except json.JSONDecodeError:
    error_message = "ACCOUNTS_JSON 参数格式错误"
    print(error_message)
    exit(1)

summary_message = "serv00-vless 恢复操作结果：\n"
default_restore_command = "cd ~/domains/$USER.serv00.net/vless && ./check_vless.sh"

# 使用 paramiko 进行 SSH 连接和执行命令
for server in servers:
    host = server['host']
    port = server['port']
    username = server['username']
    password = server['password']
    cron_command = server.get('cron', default_restore_command)
    
    print(f"连接到 {host}...")

    # 创建 SSH 客户端
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接到服务器
        client.connect(hostname=host, port=port, username=username, password=password)
        
        # 执行命令
        stdin, stdout, stderr = client.exec_command(cron_command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if output:
            summary_message += f"\n成功恢复 {host} 上的 vless 服务：\n{output}"
        if error:
            summary_message += f"\n{host} 上的 vless 服务恢复时出错：\n{error}"
    
    except paramiko.SSHException as e:
        summary_message += f"\n无法连接到 {host}：{str(e)}"
    
    finally:
        # 关闭连接
        client.close()

print(summary_message)
