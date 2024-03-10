import openai

# Set your OpenAI API key here
openai.api_key = 'your-api-key'

def generate_incident_response_playbook(threat_type, environment_details):
    """
    Generate an incident response playbook based on the provided threat type and environment details.
    """
    # Create the messages for the OpenAI API
    messages = [
        {"role": "system", "content": "You are an AI assistant helping to create an incident response playbook."},
        {"role": "user", "content": f"Create a detailed incident response playbook for handling a '{threat_type}' threat affecting the following environment: {environment_details}."}
    ]

    # Make the API call
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.7
        )
        response_content = response.choices[0].message['content'].strip()
        return response_content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Get input from the user
threat_type = input("Enter the threat type: ")
environment_details = input("Enter environment details: ")

# Generate the playbook
playbook = generate_incident_response_playbook(threat_type, environment_details)

# Print the generated playbook
if playbook:
    print("\nGenerated Incident Response Playbook:")
    print(playbook)
else:
    print("Failed to generate the playbook.")
