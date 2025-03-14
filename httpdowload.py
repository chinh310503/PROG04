import socket
import ssl

# Tạo một socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Kết nối đến máy chủ trên cổng 443 (HTTPS)
s.connect(("fullstack.edu.vn", 443))

# Gửi yêu cầu GET để tải ảnh
request = """\
GET /f8-prod/blog_posts/65/6139e2ba0f350.png HTTP/2\r\n
Host: files.fullstack.edu.vn\r\n
Cookie: _ga=GA1.1.860138504.1741937658; _ga_HZMT576BX9=GS1.1.1741937658.1.1.1741937658.0.0.0; _fbp=fb.2.1741937659909.896061575224971619\r\n
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8\r\n
Sec-Fetch-Site: same-site\r\n
Sec-Fetch-Mode: navigate\r\n
Sec-Fetch-Dest: empty\r\n
Referer: https://fullstack.edu.vn/\r\n
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36\r\n
Accept-Encoding: gzip, deflate, br\r\n
Accept-Language: en-US,en;q=0.9\r\n
Priority: u=4, i\r\n\r\n"""

s.sendall(request.encode())

# Nhận phản hồi từ máy chủ
response = b""
while True:
    data = s.recv(4096)
    if not data:
        break
    response += data
# Tách phần thân của phản hồi (nội dung của ảnh)
image_data = response.split(b"\r\n\r\n")[1]

# In ra kích thước của ảnh vừa tải
print("Kích thước của ảnh vừa tải là:", len(image_data), "bytes")
s.close()
