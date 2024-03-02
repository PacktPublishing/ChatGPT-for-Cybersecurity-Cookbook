from datetime import datetime, timedelta
import random

# Function to generate a random timestamp
def generate_timestamp(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

# Starting and ending timestamps for our log events
start_time = datetime(2024, 2, 1, 0, 0, 0)
end_time = datetime(2024, 2, 28, 23, 59, 59)

# Sample events
events = [
    "Successful user login from IP 192.168.1.10",
    "Failed user login attempt from IP 192.168.1.15",
    "High traffic detected from IP 203.0.113.5",
    "Unauthorized access attempt to server XYZ",
    "Malware detected on workstation ABC",
    "Unexpected shutdown of server XYZ",
    "Unauthorized modification of critical file /etc/passwd",
    "Data exfiltration attempt detected from IP 198.51.100.25",
    "Successful user login from IP 192.168.1.12",
    "Failed user login attempt from IP 192.168.1.18",
]

# Generate log entries
log_entries = []
for _ in range(100):  # Generating 100 log entries
    timestamp = generate_timestamp(start_time, end_time)
    event = random.choice(events)
    log_entries.append(f"[{timestamp.isoformat()}] Event: {event}")

# Sort log entries by timestamp to simulate a realistic log file
log_entries.sort()

# Joining all entries to form the log file content
log_file_content = "\n".join(log_entries)

# Displaying the first 10 lines to check the output
print("\n".join(log_entries[:10]))

# Save the log file content to a file
with open('sample_log_file.txt', 'w') as log_file:
    log_file.write(log_file_content)

