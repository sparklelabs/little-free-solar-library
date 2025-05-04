import wifi
import socketpool
import time
import os

ap_ssid = "myap"
ap_password = "password123"

def start_access_point():
    try:
        wifi.radio.stop_ap()
        time.sleep(1)
    except Exception as e:
        print("Error stopping access point:", e)

    try:
        wifi.radio.start_ap(ssid=ap_ssid, password=ap_password)
        time.sleep(5)
        print("Access point created with SSID: {}, password: {}".format(ap_ssid, ap_password))
        print("My IP address is", str(wifi.radio.ipv4_address_ap))
    except Exception as e:
        print("Error starting access point:", e)

start_access_point()

pool = socketpool.SocketPool(wifi.radio)

# Very simple MIME type guesser
def guess_type(path):
    if path.endswith(".html"):
        return "text/html"
    elif path.endswith(".txt"):
        return "text/plain"
    elif path.endswith(".jpg") or path.endswith(".jpeg"):
        return "image/jpeg"
    elif path.endswith(".png"):
        return "image/png"
    elif path.endswith(".mp3"):
        return "audio/mpeg"
    elif path.endswith(".pdf"):
        return "application/pdf"
    else:
        return "application/octet-stream"  # Fallback

def serve_file(client_socket, path):
    # Remove leading slash
    file_path = path.lstrip("/")
    if file_path == "":
        file_path = "index.html"

    content_type = guess_type(file_path)

    try:
        with open(file_path, "rb") as f:
            content = f.read()


            
        headers = (
            "HTTP/1.0 200 OK\r\n"
            "Content-Type: {}\r\n"
            "Content-Length: {}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).format(content_type, len(content))

        client_socket.sendall(headers.encode("utf-8"))
        client_socket.sendall(content)
    except Exception as e:
        print(f"Error serving {file_path}: {e}")
        error_msg = "HTTP/1.0 404 Not Found\r\nContent-Type: text/plain\r\n\r\nFile not found."
        client_socket.sendall(error_msg.encode("utf-8"))

def simple_http_server():
    server_socket = pool.socket()
    server_socket.bind(("0.0.0.0", 80))
    server_socket.listen(1)
    print("Server is listening on http://192.168.4.1")

    while True:
        print("Waiting for connection...")
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from:", client_address)

        try:
            request = client_socket.recv(1024).decode("utf-8")
            print("Request:", request)
            # Parse the GET line
            first_line = request.split("\r\n")[0]
            method, path, _ = first_line.split(" ")
            if method == "GET":
                serve_file(client_socket, path)
            else:
                client_socket.sendall(b"HTTP/1.0 405 Method Not Allowed\r\n\r\n")
        except Exception as e:
            print("Request handling failed:", e)

        client_socket.close()

simple_http_server()

