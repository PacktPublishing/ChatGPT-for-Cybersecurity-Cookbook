import openai
from openai import OpenAI # Import the OpenAI class for the new API
import os
import threading
import time
from datetime import datetime
from tqdm import tqdm

# Set up the OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
output_file = f"Cybersecurity_Awareness_Training_{current_datetime}.txt"

def content_to_text_file(slide_content: str, file):
    try:
        file.write(f"{slide_content.strip()}\n\n---\n\n")
    except Exception as e:
        print(f"An error occurred while writing the slide content: {e}")
        return False
    return True

# Function to display elapsed time while waiting for the API call
def display_elapsed_time(event):
    start_time = time.time()
    while not event.is_set():
        elapsed_time = time.time() - start_time
        print(f"\rElapsed time: {elapsed_time:.2f} seconds", end="")
        time.sleep(1)

# Create an Event object
api_call_completed = threading.Event()

# Starting the thread for displaying elapsed time
elapsed_time_thread = threading.Thread(target=display_elapsed_time, args=(api_call_completed,))
elapsed_time_thread.start()

# Prepare initial prompt
messages=[
    {
        "role": "system",
        "content": "You are a cybersecurity professional with more than 25 years of experience."
    },
    {
        "role": "user",
        "content": "Create a cybersecurity awareness training slide list that will be used for a PowerPoint slide based awareness training course, for company employees, for the electric utility industry. This should be a single level list and should not contain subsections or second-level bullets. Each item should represent a single slide."
    }
]

print(f"\nGenerating training outline...")
try:
    client = OpenAI() # Create an instance of the OpenAI class
    response = client.chat.completions.create( # Use the new API to generate the training outline
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,
    )
except Exception as e:
    print("An error occurred while connecting to the OpenAI API:", e)
    exit(1)

# Get outline
outline = response.choices[0].message.content.strip() # Updated response object attribute for the new OpenAI API

print(outline + "\n")

# Split outline into sections
sections = outline.split("\n")

# Open the output text file
try:
    with open(output_file, 'w') as file:
        # For each section in the outline
        for i, section in tqdm(enumerate(sections, start=1), total=len(sections), leave=False):
            print(f"\nGenerating details for section {i}...")

            # Prepare prompt for detailed info
            messages=[
                {
                    "role": "system",
                    "content": "You are a cybersecurity professional with more than 25 years of experience."
                },
                {
                    "role": "user",
                    "content": f"You are currently working on a PowerPoint presentation that will be used for a cybersecurity awareness training course, for end users, for the electric utility industry. The following outline is being used:\n\n{outline}\n\nCreate a single slide for the following section (and only this section) of the outline: {section}. The slides are for the employee's viewing, not the instructor, so use the appropriate voice and perspective. The employee will be using these slides as the primary source of information and lecture for the course. So, include the necessary lecture script in the speaker notes section. Do not write anything that should go in another section of the policy. Use the following format:\n\n[Title]\n\n[Content]\n\n---\n\n[Lecture]"
                }
            ]

            # Reset the Event before each API call
            api_call_completed.clear()

            try:
                response = client.chat.completions.create( # Use the new API to generate the slide content
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=2048,
                    n=1,
                    stop=None,
                    temperature=0.7,
                )
            except Exception as e:
                print("An error occurred while connecting to the OpenAI API:", e)
                exit(1)

            # Set the Event to signal that the API call is complete
            api_call_completed.set()

            # Get detailed info
            slide_content = response.choices[0].message.content.strip() # Updated response object attribute for the new OpenAI API

            # Write the slide content to the output text file
            if not content_to_text_file(slide_content, file):
                print("Failed to generate slide content. Skipping to the next section...")
                continue

    print(f"\nText file '{output_file}' generated successfully!")

except Exception as e:
    print(f"\nAn error occurred while generating the output text file: {e}")

# At the end of the script, make sure to join the elapsed_time_thread
api_call_completed.set()
elapsed_time_thread.join()