import socket
import sys
import string
import argparse
import re

def get_args():
    args = argparse.ArgumentParser()
    args.add_argument("--url")
    args.add_argument("--username")
    args.add_argument("--password")
    args.add_argument("--localfile")
    return args.parse_args()
  
args = get_args()

def get_domain(url):
    domain = ""
    if url.startswith("https://"):
        url = url[8:]
    elif url.startswith("http://"):
        url = url[7:]
    domain = url.split('/')[0]
    return domain

def recvall(s):
    total_data = []
    while True:
        data = s.recv(4096)
        if not data:
            break
        total_data.append(data.decode())
    return ''.join(total_data)

def get_cookies(res):
    cookies = []
    stringSplit = res.split("\r\n")	
    for i in stringSplit:
        if "Set-Cookie: " in i:
            cookies.append(i.split(";")[0].split(":")[1].strip())
    return ";".join(cookies)

def getWpNonce(cookies, domain, wp_path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((domain, 80))
    req = f"GET {wp_path}/wp-admin/media-new.php HTTP/1.1\r\nHost: {domain}\r\nCookie: {cookies}\r\n\r\n"
    s.send(req.encode())
    res = recvall(s)
    s.close()
    match = re.search('name="_wpnonce" value="([a-f0-9]+)"', res)
    if match:
        return match.group(1)
    else:
        print("Failed to find wpnonce")
        exit(1)

def upload_image(cookies, domain, wp_path, fileName, pathLocalFile):
    with open(pathLocalFile, 'rb') as f:
        data = f.read()
    
    wpnonce = getWpNonce(cookies, domain, wp_path)
    content_type = fileName.split(".")[-1].lower()
    
    boundary = "----WebKitFormBoundary"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="name"\r\n\r\n'
        f'{fileName}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="action"\r\n\r\n'
        f'upload-attachment\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="_wpnonce"\r\n\r\n'
        f'{wpnonce}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="async-upload"; filename="{fileName}"\r\n'
        f'Content-Type: image/{content_type}\r\n\r\n'
    ).encode() + data + f"\r\n--{boundary}--\r\n".encode()
    
    headers = (
        f"POST {wp_path}/wp-admin/async-upload.php HTTP/1.1\r\n"
        f"Host: {domain}\r\n"
        f"Cookie: {cookies}\r\n"
        f"Content-Type: multipart/form-data; boundary={boundary}\r\n"
        f"Content-Length: {len(body)}\r\n\r\n"
    )
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((domain, 80))
    s.send(headers.encode() + body)
    res = recvall(s)
    s.close()
    
    if "HTTP/1.1 200 OK" in res and "{\"success\":true" in res:
        print("Upload success.")
        match = re.search(r'"url":"([^"]+)"', res)
        if match:
            print(f"File upload url: {match.group(1).replace('\\', '')}")
    else:
        print("Upload fail.")
        print(res)

# Main execution
url = args.url
username = args.username
password = args.password
pathLocalFile = args.localfile
domain = get_domain(url)
wp_path = '/wordpress'  # Đường dẫn cố định đến thư mục WordPress
fileName = pathLocalFile.split("/")[-1]

# Đăng nhập
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((domain, 80))
login_body = f"log={username}&pwd={password}&wp-submit=Log+In"
headers = (
    f"POST {wp_path}/wp-login.php HTTP/1.1\r\n"
    f"Host: {domain}\r\n"
    f"Content-Length: {len(login_body)}\r\n"
    f"Content-Type: application/x-www-form-urlencoded\r\n"
    f"Connection: close\r\n\r\n"
)
s.send(headers.encode() + login_body.encode())
res = recvall(s)
s.close()

if "HTTP/1.1 302 Found" in res and "is incorrect" not in res:
    cookies = get_cookies(res)
    upload_image(cookies, domain, wp_path, fileName, pathLocalFile)
else:
    print("Đăng nhập thất bại")
    exit(1)
