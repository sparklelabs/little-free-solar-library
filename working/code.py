import wifi
import socketpool
import time

# set access point credentials
ap_ssid = "myap"
ap_password = "password123"  # not used

# Function to start the access point
def start_access_point():
    # Stop any existing access point
    try:
        wifi.radio.stop_ap()
        time.sleep(1)  # Allow some time for it to shut down
    except Exception as e:
        print("Error stopping access point:", e)

    # Start the access point
    try:
        wifi.radio.start_ap(ssid=ap_ssid, password=ap_password)
        time.sleep(5)  # Give it some time to start properly
        print("Access point created with SSID: {}, password: {}".format(ap_ssid, ap_password))
        print("My IP address is", str(wifi.radio.ipv4_address_ap))
    except Exception as e:
        print("Error starting access point:", e)

start_access_point()

# create a socket pool
pool = socketpool.SocketPool(wifi.radio)

# function to read file content
def read_file(file_name):
    try:
        with open(file_name, 'rb') as f:  # Open in binary mode for MP3
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def simple_http_server():
    server_socket = pool.socket()
    server_socket.bind(("0.0.0.0", 80))
    server_socket.listen(1)

    print("server is listening on {}:80".format(wifi.radio.ipv4_address_ap))

    while True:
        print("waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print("accepted connection from:", client_address)

        try:
            buffer = bytearray(1024)
            bytes_received = client_socket.recv_into(buffer)
            request = buffer[:bytes_received].decode("utf-8")
            print("Request received:", request)

            # Parse the requested file from the HTTP request
            request_line = request.split("\r\n")[0]
            requested_file = request_line.split(" ")[1].lstrip("/")
            if requested_file == "":  # Default to index.html
                requested_file = "index.html"

            # Determine content type
            if requested_file.endswith(".mp3"):
                content_type = "audio/mpeg"
            elif requested_file.endswith(".html"):
                content_type = "text/html"
            else:
                content_type = "application/octet-stream"

            # Read the requested file
            file_content = read_file(requested_file)
            if file_content is None:
                # File not found or error
                http_response = "HTTP/1.0 404 Not Found\r\n\r\nFile not found"
                client_socket.sendall(http_response.encode("utf-8"))
            else:
                # Send the response with the correct content type
                http_response = f"HTTP/1.0 200 OK\r\nContent-Type: {content_type}\r\n\r\n"
                client_socket.sendall(http_response.encode("utf-8"))
                client_socket.sendall(file_content)

        except Exception as e:
            print("Error handling request:", e)

        # Close the client socket
        client_socket.close()
        print("response sent to:", client_address)


# start the http server
simple_http_server()
