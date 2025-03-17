import socket

# Dữ liệu POST

data = 'log=wordpressuser&pwd=TranVanChinh2003&wp-submit=Log+In'

# Tạo một socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Kết nối đến máy chủ
s.connect(('localhost', 80))

# Gửi yêu cầu POST đến máy chủ
request = f"POST /wordpress/wp-login.php HTTP/1.1\r\n"
request += "Host: tvc1\r\n"
request += f"Content-Length: {len(data)}\r\n"
request += "Cache-Control: max-age=0\r\n"
request += 'Sec-Ch-Ua: "Chromium";v="119", "Not?A_Brand";v="24"\r\n'
request += "Sec-Ch-Ua-Mobile: ?0\r\n"
request += 'Sec-Ch-Ua-Platform: "Linux"\r\n'
request += "Upgrade-Insecure-Requests: 1\r\n"
request += "Content-Type: application/x-www-form-urlencoded\r\n"
request += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36\r\n"
request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\n"
request += "Sec-Fetch-Site: same-origin\r\n"
request += "Sec-Fetch-Mode: navigate\r\n"
request += "Sec-Fetch-User: ?1\r\n"
request += "Sec-Fetch-Dest: document\r\n"
request += "Referer: http://localhost/test-socket/\r\n"
request += "Accept-Encoding: gzip, deflate, br\r\n"
request += "Accept-Language: en-US,en;q=0.9\r\n"
request += "\r\n"
request += data

s.send(request.encode())

# Nhận phản hồi từ máy chủ
response = b""
while True:
    data = s.recv(4096)
    if not data:
        break
    response += data

if b"302 Found" in response:
    print("Dang nhap thanh cong")
else:
    print("Dang nhap that bai")

s.close()
