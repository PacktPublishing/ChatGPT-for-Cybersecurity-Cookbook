import subprocess
import os
import openai

# Initialize the OpenAI API client
#openai.api_key = 'YOUR_OPENAI_API_KEY'  # Replace with your actual API key or use a system environment variable as shown below
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

# Function to run a command and return its output
def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    return result.stdout

# Gather data from key locations
registry_data = run_command('reg query HKLM /s')  # Replace with specific registry keys
process_data = run_command('tasklist /v')
network_data = run_command('netstat -an')
scheduled_tasks = run_command('schtasks /query /fo LIST')
security_logs = run_command('wevtutil qe Security /c:1 /rd:true /f:text')  # Last security event

# Analyze the gathered data using ChatGPT
analysis_result = call_gpt(f"Analyze the following Windows system data for signs of APTs:\nRegistry Data:\n{registry_data}\n\nProcess Data:\n{process_data}\n\nNetwork Data:\n{network_data}\n\nScheduled Tasks:\n{scheduled_tasks}\n\nSecurity Logs:\n{security_logs}")

# Display the analysis result
print(f"Analysis Result:\n{analysis_result}")
