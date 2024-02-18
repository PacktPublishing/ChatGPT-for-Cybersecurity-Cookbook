import openai
import os

# Initialize the OpenAI API client
openai.api_key = os.getenv("OPENAI_API_KEY")

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

def analyze_threat_data(file_path):
    # Read the raw threat data from the provided file
    with open(file_path, 'r') as file:
        raw_data = file.read()

    # Query ChatGPT to identify and categorize potential threats
    identified_threats = call_gpt(f"Analyze the following threat data and identify potential threats: {raw_data}")

    # Extract IoCs from the threat data
    extracted_iocs = call_gpt(f"Extract all indicators of compromise (IoCs) from the following threat data: {raw_data}")

    # Obtain a detailed context or narrative behind the identified threats
    threat_context = call_gpt(f"Provide a detailed context or narrative behind the identified threats in this data: {raw_data}")

    # Print the results
    print("Identified Threats:", identified_threats)
    print("\nExtracted IoCs:", extracted_iocs)
    print("\nThreat Context:", threat_context)

if __name__ == "__main__":
    file_path = input("Enter the path to the raw threat data .txt file: ")
    analyze_threat_data(file_path)
