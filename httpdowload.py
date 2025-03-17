import socket

# Thông tin máy chủ và đường dẫn ảnh
HOST = "tvc1"
PORT = 80  # HTTP sử dụng cổng 80
IMAGE_PATH = "/wordpress/wp-content/uploads/2025/03/Flag_of_Vietnam.svg_.png"

# Tạo socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Gửi yêu cầu GET để tải ảnh
request = f"""\
GET {IMAGE_PATH} HTTP/1.1\r\n\
Host: {HOST}\r\n\
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.123 Safari/537.36\r\n\
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8\r\n\
Accept-Encoding: identity\r\n\
Connection: close\r\n\r\n\
"""

s.sendall(request.encode())

# Nhận phản hồi từ máy chủ
response = b""
while True:
    data = s.recv(4096)
    if not data:
        break
    response += data

s.close()

header, image_data = response.split(b"\r\n\r\n", 1)

print("Kích thước của ảnh vừa tải là:", len(image_data), "bytes")

# Kiểm tra xem phản hồi
if b"200 OK" not in header:
    print("Lỗi tải ảnh, kiểm tra lại URL!")
else:
    # Lưu ảnh vào file
    with open("Flag_of_Vietnam.png", "wb") as file:
        file.write(image_data)
    print("Tải ảnh thành công, đã lưu vào Flag_of_Vietnam.png")
