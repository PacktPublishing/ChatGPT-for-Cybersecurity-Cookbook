import openai
import os
import threading
import time
from datetime import datetime

# Set up the OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
assessment_name = f"Exam_questions_{current_datetime}.txt"

def generate_email_simulations() -> str:
    # Define the conversation messages
    messages = [
        {"role": "system", "content": 'You are a cybersecurity professional and training instructor with more than 25 years of experience.'},
        {"role": "user", "content": 'Help me study for the CISSP exam. Generate a list of 25 multiple choice questions, just as they will appear on the exam or practice exams. Present the question follow by the answer choices. After all of the questions have been listed, automatically provide an answer key without waiting for a prompt.'},
    ]

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Return the generated text
    return response['choices'][0]['message']['content'].strip()

# Function to display elapsed time while waiting for the API call
def display_elapsed_time():
    start_time = time.time()
    while not api_call_completed:
        elapsed_time = time.time() - start_time
        print(f"\rElapsed time: {elapsed_time:.2f} seconds", end="")
        time.sleep(1)

api_call_completed = False
elapsed_time_thread = threading.Thread(target=display_elapsed_time)
elapsed_time_thread.start()

# Generate the report using the OpenAI API
try:
    # Generate the email simulations
    email_simulations = generate_email_simulations()
except Exception as e:
    print(f"\nAn error occurred during the API call: {e}")
    api_call_completed = True
    exit()  

api_call_completed = True
elapsed_time_thread.join()

# Save the email simulations into a text file
try:
    with open(assessment_name, 'w') as file:
        file.write(email_simulations)
    print("\nEmail simulations generated successfully!")
except Exception as e:
    print(f"\nAn error occurred during the email simulations generation: {e}")