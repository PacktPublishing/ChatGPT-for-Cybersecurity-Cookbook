from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

# Function to create an OpenAI assistant
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a cybersecurity professional.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-turbo-preview"
)




# Function to submit cybersecurity-related queries
def submit_cybersecurity_query(assistant_id, thread, query):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=query
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

# Function to retrieve responses from the assistant
def get_cybersecurity_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

# Function to create a thread and submit a query
def create_thread_and_query(assistant_id, user_input):
    thread = client.beta.threads.create()
    run = submit_cybersecurity_query(assistant_id, thread, user_input)
    return thread, run

# Example usage
CYBERSECURITY_ASSISTANT_ID = "your-assistant-id"  # Replace with your actual Assistant ID
thread1, run1 = create_thread_and_query(
    CYBERSECURITY_ASSISTANT_ID,
    "Can you analyze this suspicious network traffic pattern?"
)

# Add Additional example code to wait for and retrieve responses
response1 = get_cybersecurity_response(thread1)
print(response1)

