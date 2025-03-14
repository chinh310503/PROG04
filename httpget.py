import socket
import sys

def get_title(url):
    # Tách tên miền và đường dẫn từ URL
    parts = url.split('/')
    domain = parts[2]
    path = '/' + '/'.join(parts[3:])
    # Tạo kết nối socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((domain, 80))

    # Gửi yêu cầu GET
    request = f"GET {path} HTTP/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n"
    s.sendall(request.encode())
    # Nhận và xử lý phản hồi
    response = b""
    while True:
        data = s.recv(1024)
        if not data:
            break
        response += data

    # Tìm title trong phản hồi
    title_start = response.find(b"<title>") + len(b"<title>")
    title_end = response.find(b"</title>", title_start)
    title = response[title_start:title_end].decode()

    # In ra title
    print("Title:", title)

    s.close()

get_title('http://example.com/')