from scapy.all import rdpcap, IP, TCP
import os
import openai

# Initialize the OpenAI API client
#openai.api_key = 'YOUR_OPENAI_API_KEY'  # Replace with your actual API key or set the OPENAI_API_KEY environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  

# Function to interact with ChatGPT
def chat_with_gpt(prompt):
    messages = [
        {
            "role": "system",
            "content": "You are a cybersecurity SOC analyst with more than 25 years of experience."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

# Read PCAP file
packets = rdpcap('example.pcap')

# Summarize the traffic (simplified example)
ip_summary = {}
port_summary = {}
protocol_summary = {}

for packet in packets:
    if packet.haslayer(IP):
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        ip_summary[f"{ip_src} to {ip_dst}"] = ip_summary.get(f"{ip_src} to {ip_dst}", 0) + 1

    if packet.haslayer(TCP):
        port_summary[packet[TCP].sport] = port_summary.get(packet[TCP].sport, 0) + 1

    if packet.haslayer(IP):
        protocol_summary[packet[IP].proto] = protocol_summary.get(packet[IP].proto, 0) + 1

# Create summary strings
ip_summary_str = "\n".join(f"{k}: {v} packets" for k, v in ip_summary.items())
port_summary_str = "\n".join(f"Port {k}: {v} packets" for k, v in port_summary.items())
protocol_summary_str = "\n".join(f"Protocol {k}: {v} packets" for k, v in protocol_summary.items())

# Combine summaries
total_summary = f"IP Summary:\n{ip_summary_str}\n\nPort Summary:\n{port_summary_str}\n\nProtocol Summary:\n{protocol_summary_str}"

# Analyze using ChatGPT
analysis_result = chat_with_gpt(f"Analyze the following summarized network traffic for anomalies or potential threats:\n{total_summary}")

# Print the analysis result
print(f"Analysis Result:\n{analysis_result}")
