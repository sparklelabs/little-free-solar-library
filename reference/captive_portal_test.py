import wifi
import socketpool
import time
import os
from adafruit_httpserver import Server, Request, Response

# 1. Start the Access Point
SSID = "Solar_Library_Free"
PASSWORD = None  # Open network so users don't need a password

print("Starting Wi-Fi Access Point...")
try:
    wifi.radio.stop_ap()
    time.sleep(1)
except Exception:
    pass

wifi.radio.start_ap(ssid=SSID)
my_ip = str(wifi.radio.ipv4_address_ap)
print(f"AP active. SSID: {SSID}")
print(f"Board IP: {my_ip}")

# 2. Setup Socket Pool and Web Server
pool = socketpool.SocketPool(wifi.radio)
web_server = Server(pool, debug=True)

# HTML Landing Page
LANDING_PAGE_HTML = """<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solar Little Library</title>
    <style>
        body { font-family: -apple-system, sans-serif; text-align: center; padding: 20px; background-color: #f4f4f9; color: #333; }
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 400px; margin: 0 auto; }
        h1 { color: #e0a458; }
        .instructions { background: #eef2f3; padding: 15px; border-radius: 8px; font-size: 14px; text-align: left; }
        a { display: inline-block; background: #e0a458; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Solar Little Library</h1>
        <p>You have connected to the offline library server!</p>
        
        <div class="instructions">
            <strong>CRITICAL STEP FOR PHONES:</strong><br>
            Modern phones block downloading books directly inside this automatic popup window.<br><br>
            1. Copy this link: <strong>http://192.168.4.1</strong><br>
            2. Open your standard browser (Safari/Chrome).<br>
            3. Paste the link and press enter to browse and download.
        </div>
        <a href="http://192.168.4.1">Open in Browser</a>
    </div>
</body>
</html>
"""

# Route for default landing page
@web_server.route("/")
def root_route(request: Request):
    return Response(request, content_type="text/html", body=LANDING_PAGE_HTML)

# Handle Android connectivity checks
@web_server.route("/generate_204")
def android_connectivity_route(request: Request):
    print("Android connectivity check intercepted")
    # Redirecting to root triggers the captive portal login popup on Android
    return Response(request, content_type="text/html", body=LANDING_PAGE_HTML)

# Handle Apple connectivity checks (hotspot-detect)
@web_server.route("/hotspot-detect.html")
def apple_connectivity_route(request: Request):
    print("iOS connectivity check intercepted")
    return Response(request, content_type="text/html", body=LANDING_PAGE_HTML)

# Start web server non-blocking
web_server.start(host=my_ip, port=80)
print(f"Web server started on http://{my_ip}:80")

# 3. DNS Redirect Server (UDP Port 53)
# Intercepts all DNS requests and responds with the ESP32-S3's IP
dns_sock = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
dns_sock.setblocking(False)
dns_sock.bind((my_ip, 53))
print("DNS server listening on port 53...")

def make_dns_response(query_data, ip_address):
    tid = query_data[0:2]
    flags = b'\x81\x80'  # Standard response, no error
    qdcount = query_data[4:6]
    ancount = b'\x00\x01'  # 1 Answer record
    nscount = b'\x00\x00'
    arcount = b'\x00\x00'
    
    # Locate end of QNAME
    ptr = 12
    while query_data[ptr] != 0:
        ptr += query_data[ptr] + 1
    ptr += 5 # Skip terminator, QTYPE, and QCLASS
    
    question_sec = query_data[12:ptr]
    ans_name = b'\xc0\x0c' # Pointer to query name at offset 12
    ans_type = b'\x00\x01' # Type A (IPv4)
    ans_class = b'\x00\x01' # Class IN
    ans_ttl = b'\x00\x00\x00\x3c' # 60 seconds
    ans_rdlength = b'\x00\x04' # 4 bytes
    
    ip_bytes = bytes([int(x) for x in ip_address.split('.')])
    
    return tid + flags + qdcount + ancount + nscount + arcount + question_sec + ans_name + ans_type + ans_class + ans_ttl + ans_rdlength + ip_bytes

# Run loops
dns_buffer = bytearray(512)
while True:
    # 1. Handle DNS queries
    try:
        size, addr = dns_sock.recvfrom_into(dns_buffer)
        query = dns_buffer[:size]
        response = make_dns_response(query, my_ip)
        dns_sock.sendto(response, addr)
        print(f"DNS redirected query from {addr}")
    except OSError:
        pass  # Non-blocking socket empty

    # 2. Poll Web Server
    try:
        web_server.poll()
    except Exception as e:
        print(f"Web server error: {e}")
        
    time.sleep(0.01)
