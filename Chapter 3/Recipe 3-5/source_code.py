import socket
import concurrent.futures

target = input("Enter target IP address: ")
start_port = int(input("Enter start port number: "))
end_port = int(input("Enter end port number: "))

def grab_banner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024).decode().strip('\n').strip('\r')
        s.close()
        return banner
    except:
        return "No banner could be grabbed"

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            banner = grab_banner(target, port)
            print(f"Port {port} is open: {banner}")
        sock.close()
    except KeyboardInterrupt:
        print("\n Exiting Program !!!!")
        exit()
    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        exit()
    except socket.error:
        print("\ Server not responding !!!!")
        exit()

def scan_ports(target, start_port, end_port):
    print(f"Starting scan on host: {target}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, port)

print("-" * 50)
print("Simple Port Scanner")
print("-" * 50)

scan_ports(target, start_port, end_port)
