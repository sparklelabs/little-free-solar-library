import wifi
import socketpool
import time

# set access point credentials
ap_ssid = "myap"
ap_password = "password123" # not used

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

# function to read html content from a file
def read_html_file(file_name):
    try:
        with open(file_name, 'r') as f:
            return f.read()
    except exception as e:
        print(f"error reading file: {e}")
        return "<html><body><h1>error loading page</h1></body></html>"

# create a simple http server function
def simple_http_server():
    server_socket = pool.socket()
    # bind the server socket to the pico's ip address and port 80
    server_socket.bind((str(wifi.radio.ipv4_address_ap), 80))  # convert ip address to string
    server_socket.listen(1)

    print("server is listening on {}:80".format(wifi.radio.ipv4_address_ap))

    while True:
        print("waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print("accepted connection from:", client_address)

        # http response
        http_response = "http/1.0 200 ok\r\ncontent-type: text/html\r\n\r\n"
        # html_content = "<html><body><h1>hello, world!</h1></body></html>\r\n"
        html_content = read_html_file('index.html')

        # send the response headers and content
        client_socket.sendall(http_response.encode("utf-8"))
        client_socket.sendall(html_content.encode("utf-8"))

        # close the client socket
        client_socket.close()
        print("response sent to:", client_address)

# start the http server
simple_http_server()
