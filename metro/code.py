# CircuitPython Captive Portal & Web Server
# Project: Solar Little Library
#
# INSTRUCTIONS:
# 1. Copy this file to your Metro ESP32-S3 as `code.py`.
# 2. Make sure you have the `adafruit_httpserver` library copied into your Metro's `lib/` directory.
#    You can download it from the Adafruit CircuitPython Bundle (https://circuitpython.org/libraries).

import wifi
import socketpool
import time
from adafruit_httpserver import Server, Request, Response, FileResponse

# --- 1. CONFIGURATION ---
SSID = "Solar_Library_Free"
PORTAL_IP = "192.168.4.1"

# --- 2. START ACCESS POINT ---
print("Configuring Wi-Fi Access Point...")
try:
    wifi.radio.stop_ap()
    time.sleep(0.5)
except Exception:
    pass

# Start AP mode
wifi.radio.start_ap(ssid=SSID)

# Wait for IP address to be assigned (ESP32-S3 DHCP server initialization takes a moment)
print("Waiting for IP address allocation...")
timeout = 10
while wifi.radio.ipv4_address_ap is None and timeout > 0:
    time.sleep(0.5)
    timeout -= 1

if wifi.radio.ipv4_address_ap is None:
    my_ip = "192.168.4.1"  # Fallback to standard default AP IP
else:
    my_ip = str(wifi.radio.ipv4_address_ap)

print(f"AP Active! SSID: {SSID}")
print(f"Server IP address is {my_ip}")

# --- 3. HTTP SERVER SETUP ---
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, root_path="/", debug=True)

# Web Server Routes
@server.route("/")
def root_handler(request: Request):
    return FileResponse(request, "index.html")

# Captive Portal detection probes (Android & Apple)
@server.route("/generate_204")
def android_probe_handler(request: Request):
    print("Android probe intercepted.")
    return FileResponse(request, "index.html")

@server.route("/hotspot-detect.html")
def ios_probe_handler(request: Request):
    print("iOS probe intercepted.")
    return FileResponse(request, "index.html")

# Start web server non-blocking
server.start(host=my_ip, port=80)
print(f"Web server listening on port 80...")

# --- 4. DNS REDIRECTOR SETUP (UDP PORT 53) ---
# Intercepts all DNS requests and points them back to the ESP32-S3
dns_socket = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
dns_socket.setblocking(False)
dns_socket.bind((my_ip, 53))
print("DNS Redirector listening on port 53...")

def make_dns_response(query_data, redirect_ip):
    """
    Constructs a spoofed DNS response mapping any requested host to the redirect IP.
    """
    transaction_id = query_data[0:2]
    flags = b'\x81\x80'      # Flags: Standard query response, no error
    qdcount = query_data[4:6]
    ancount = b'\x00\x01'    # 1 Answer record
    nscount = b'\x00\x00'
    arcount = b'\x00\x00'
    
    # Traverse query name to find end of question section
    ptr = 12
    while query_data[ptr] != 0:
        ptr += query_data[ptr] + 1
    ptr += 5  # Skip terminator, QTYPE, and QCLASS
    
    question_section = query_data[12:ptr]
    
    # Construct Answer Record
    ans_name = b'\xc0\x0c'         # Pointer to domain name in question section
    ans_type = b'\x00\x01'         # Type A (IPv4)
    ans_class = b'\x00\x01'        # Class IN (Internet)
    ans_ttl = b'\x00\x00\x00\x3c'  # TTL: 60 seconds
    ans_rdlength = b'\x00\x04'     # IP length: 4 bytes
    
    # Parse target IP into bytes
    ip_bytes = bytes([int(x) for x in redirect_ip.split('.')])
    
    return transaction_id + flags + qdcount + ancount + nscount + arcount + question_section + ans_name + ans_type + ans_class + ans_ttl + ans_rdlength + ip_bytes

# --- 5. MAIN EXECUTION LOOP ---
dns_buffer = bytearray(512)
while True:
    # Handle incoming DNS queries (non-blocking check)
    try:
        size, sender_addr = dns_socket.recvfrom_into(dns_buffer)
        query = dns_buffer[:size]
        response = make_dns_response(query, my_ip)
        dns_socket.sendto(response, sender_addr)
        print(f"DNS Redirect: intercepted request from {sender_addr}")
    except OSError:
        pass  # Socket was empty, continue

    # Poll Web Server for requests
    try:
        server.poll()
    except Exception as e:
        print(f"Web Server Error: {e}")

    time.sleep(0.01)
