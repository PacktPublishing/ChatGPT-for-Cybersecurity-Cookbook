import openai
from openai import OpenAI  # Updated for the new OpenAI API
import re
import os
import numpy as np
import faiss  # Make sure FAISS is installed

client = OpenAI()  # Updated for the new OpenAI API

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

def get_embeddings(texts):
    """
    Fetches embeddings for a list of texts using the OpenAI API.
    """
    response = client.Embedding.create(
        model="text-embedding-ada-002",
        input=texts
    )
    return np.array([item['embedding'] for item in response['data']])

def create_faiss_index(embeddings):
    """
    Creates a FAISS index for a given set of embeddings.
    """
    d = embeddings.shape[1]  # Dimensionality of the embeddings
    index = faiss.IndexFlatL2(d)
    index.add(embeddings.astype(np.float32))  # FAISS expects float32
    return index

def analyze_logs_with_embeddings(log_data):
    """
    Analyze log data using OpenAI embeddings and FAISS to categorize events.
    """
    # Define your templates
    suspicious_templates = ["Unauthorized access attempt detected", "Multiple failed login attempts"]
    normal_templates = ["User logged in successfully", "System health check completed"]

    # Compute embeddings for templates
    suspicious_embeddings = get_embeddings(suspicious_templates)
    normal_embeddings = get_embeddings(normal_templates)

    # Combine all template embeddings and create a FAISS index
    template_embeddings = np.vstack((suspicious_embeddings, normal_embeddings))
    index = create_faiss_index(template_embeddings)

    # Labels for each template
    labels = ['Suspicious'] * len(suspicious_embeddings) + ['Normal'] * len(normal_embeddings)

    categorized_events = []

    for entry in log_data:
        log_embedding = get_embeddings([entry["Event"]]).astype(np.float32)
        k = 1  # Number of nearest neighbors to find
        _, indices = index.search(log_embedding, k)
        category = labels[indices[0][0]]
        categorized_events.append((entry["Timestamp"], entry["Event"], category))

    return categorized_events

# Sample raw log file path
raw_log_file_path = 'sample_log_file.txt'

# Parse the raw log file into JSON format
log_data = parse_raw_log_to_json(raw_log_file_path)

# Analyze the logs
categorized_timeline = analyze_logs_with_embeddings(log_data)

# Print the categorized timeline
for timestamp, event, category in categorized_timeline:
    print(f"{timestamp} - {event} - {category}")
