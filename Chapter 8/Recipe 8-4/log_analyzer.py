import openai
import json
import re
import os

# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_raw_log_to_json(raw_log_path):
    """
    Parses a raw log file and converts it into a JSON format.
    """
    # Regular expressions to match timestamps and event descriptions in the raw log
    timestamp_regex = r'\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\]'
    event_regex = r'Event: (.+)'

    json_data = []

    with open(raw_log_path, 'r') as file:
        for line in file:
            timestamp_match = re.search(timestamp_regex, line)
            event_match = re.search(event_regex, line)

            if timestamp_match and event_match:
                timestamp = timestamp_match.group().strip('[]')
                event_description = event_match.group(1)
                json_data.append({"Timestamp": timestamp, "Event": event_description})
    
    return json_data

def analyze_logs_with_embeddings(log_data):
    """
    Analyze log data using OpenAI embeddings to categorize events.
    """
    categorized_events = []
    for entry in log_data:
        # Generate embeddings for each log entry
        response = openai.Embedding.create(
            model="text-similarity-davinci-001",
            input=entry["Event"]
        )
        embedding = response['data'][0]['embedding']
        
        # Categorize events based on embeddings (placeholder for actual logic)
        category = "Suspicious Activity" if sum(embedding) > 0 else "Normal Activity"  # Simplified example
        categorized_events.append((entry["Timestamp"], entry["Event"], category))
    
    return categorized_events

# Sample raw log file path
raw_log_file_path = 'path_to_your_raw_log_file.txt'

# Parse the raw log file into JSON format
log_data = parse_raw_log_to_json(raw_log_file_path)

# Analyze the logs
categorized_timeline = analyze_logs_with_embeddings(log_data)

# Print the categorized timeline
for timestamp, event, category in categorized_timeline:
    print(f"{timestamp} - {event} - {category}")
