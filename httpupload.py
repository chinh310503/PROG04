import socket
import ssl
import os

def create_multipart_form_data(file_path, boundary):
    """Tạo dữ liệu multipart/form-data để upload file"""
    file_name = os.path.basename(file_path)

    with open(file_path, 'rb') as file:
        file_data = file.read()

    form_data = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{file_name}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()

    return form_data

def send_post_request(host, path, file_path):
    """Gửi request POST để upload file bằng socket"""
    port = 443  # HTTPS
    boundary = "----WebKitFormBoundaryX1a2b3c4d5e6f7g8h"

    # Tạo nội dung request
    form_data = create_multipart_form_data(file_path, boundary)
    content_length = len(form_data)

    request_headers = (
        f"POST {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "User-Agent: Python-Socket-Upload\r\n"
        "Accept: */*\r\n"
        "Connection: close\r\n"
        f"Content-Type: multipart/form-data; boundary={boundary}\r\n"
        f"Content-Length: {content_length}\r\n"
        "\r\n"
    ).encode()

    # Kết nối socket với SSL
    s = socket.create_connection((host, port))
    ssl_socket = ssl.create_default_context().wrap_socket(s, server_hostname=host)

    # Gửi request
    ssl_socket.sendall(request_headers + form_data)

    # Nhận phản hồi từ server
    response = b""
    while True:
        data = ssl_socket.recv(4096)
        if not data:
            break
        response += data

    ssl_socket.close()
    return response.decode()

if __name__ == "__main__":
    host = "postman-echo.com"
    path = "/post"  
    file_path = "test.png" 

    response = send_post_request(host, path, file_path)
    print(response)
