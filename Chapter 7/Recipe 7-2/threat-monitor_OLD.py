import asyncio
import openai
import os
import socket
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Initialize the OpenAI API client
#openai.api_key = 'YOUR_OPENAI_API_KEY'  # Replace with your actual API key if you choose not to use a system environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to interact with ChatGPT
def call_gpt(prompt):
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

# Asynchronous function to handle incoming syslog messages
async def handle_syslog():
    UDP_IP = "0.0.0.0"
    UDP_PORT = 514

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        log_entry = data.decode('utf-8')
        analysis_result = call_gpt(f"Analyze the following log entry for potential threats: {log_entry} \n\nIf you believe there may be suspicious activity, start your response with 'Suspicious Activity: ' and then your analysis. Provide nothing else.")

        if "Suspicious Activity" in analysis_result:
            print(f"Alert: {analysis_result}")

        await asyncio.sleep(0.1)  # A small delay to allow other tasks to run

# Class to handle file system events
class Watcher:
    DIRECTORY_TO_WATCH = "/path/to/log/directory"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                pass
        except:
            self.observer.stop()
            print("Observer stopped")

class Handler(FileSystemEventHandler):
    def process(self, event):
        if event.is_directory:
            return
        elif event.event_type == 'created':
            print(f"Received file: {event.src_path}")
            with open(event.src_path, 'r') as file:
                for line in file:
                    analysis_result = call_gpt(f"Analyze the following log entry for potential threats: {line.strip()} \n\nIf you believe there may be suspicious activity, start your response with 'Suspicious Activity: ' and then your analysis. Provide nothing else.")

                    if "Suspicious Activity" in analysis_result:
                        print(f"Alert: {analysis_result}")

    def on_created(self, event):
        self.process(event)

if __name__ == "__main__":
    # Start the syslog handler
    asyncio.run(handle_syslog())

    # Start the directory watcher
    w = Watcher()
    w.run()
