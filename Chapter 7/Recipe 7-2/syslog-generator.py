# This script generates simulated syslog messages and sends them to a syslog server to test the code for this recipe.
# This script can be found in the GitHub repository for this book/recipe: https://github.com/PacktPublishing/ChatGPT-for-Cybersecurity-Cookbook/tree/main/Chapter%207/Recipe%207-2

import socket
import time
from random import choice, randint

def generate_network_switch_syslog():
    # Standard operational messages
    normal_events = [
        'Interface GigabitEthernet1/0/24 is up',
        'Configured from console by admin on vty0 (192.168.1.5)',
        'Interface GigabitEthernet1/0/24, changed state to up',
        'VLAN 20 added to interface GigabitEthernet1/0/24',
        'STP changed state to forwarding on GigabitEthernet1/0/24'
    ]

    # Suspicious or potentially harmful activities
    suspicious_events = [
        'Unauthorized access attempt on console port',
        'Configuration changed by unknown user on vty1 (192.168.1.100)',
        'Interface GigabitEthernet1/0/24, changed state to down - possible cable tampering detected',
        'Multiple failed login attempts detected on vty2 (192.168.1.6)',
        'Unusual traffic pattern detected from GigabitEthernet1/0/24 - possible DDoS attack'
    ]

    # Choose whether to generate a normal or suspicious event
    if randint(0, 10) < 8:  # 80% chance to generate normal events
        event = choice(normal_events)
        severity = 'INFO'
    else:  # 20% chance to generate suspicious events
        event = choice(suspicious_events)
        severity = 'WARNING'

    # Create a timestamp
    timestamp = time.strftime("%b %d %H:%M:%S")

    # Create a simulated switch name
    switch_name = f'switch{randint(1, 50)}'

    # Construct the syslog message
    syslog_message = f"{timestamp} {switch_name} %LINK-{severity}: {event}"

    return syslog_message

def send_syslog_messages(ip, port, message_count=50):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        for _ in range(message_count):
            message = generate_network_switch_syslog()
            sock.sendto(message.encode('utf-8'), (ip, port))
            print(f"Sent: {message}")
            time.sleep(1)  # Wait a second between messages
    finally:
        sock.close()

# Replace with your syslog server IP and port
send_syslog_messages('127.0.0.1', 514)