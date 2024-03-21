import openai
from openai import OpenAI
import os
import subprocess

client = OpenAI() # Create a new OpenAI client
conversation_history = [{"role": "system", "content": "You are a Kali Linux expert. When I give you a prompt, provide me with the Kali Linux command necessary to complete the request. Use all conversation history as reference as needed. (Assume I have all necessary apps, tools, and commands necessary to complete the request. Provide me with ONLY THE COMMAND and DO NOT generate anything before or further beyond the command. DO NOT provide back ticks around the command. DO NOT provide any explanation. Provide the simplest form of the command possible unless I ask for special options, considerations, output, etc. If the request does require a compound command, provide all necessary operators, options, pipes, etc. as a single one-line command. Do not provide me more than one variation or more than one line. DO NOT provide markdown. Just provie the command as plain text.)"}]

def open_file(filepath): #Open and read a file
    with open(filepath, 'r', encoding='UTF-8') as infile:
        return infile.read()
        
def save_file(filepath, content): #Create a new file or overwrite an existing one.
    with open(filepath, 'w', encoding='UTF-8') as outfile:
        outfile.write(content)

def append_file(filepath, content): #Create a new file or append an existing one.
    with open(filepath, 'a', encoding='UTF-8') as outfile:
        outfile.write(content)

openai.api_key = os.getenv("OPENAI_API_KEY") #Use this if you prefer to use the key in an environment variable.        
#openai.api_key = open_file('openai-key.txt') #Grabs your OpenAI key from a file
        
def gpt(conversation_history): #Sets up and runs the request to the OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=conversation_history,
            temperature=0.1,
        )
        response_text = response.choices[0].message.content.strip()
        return response_text
    except openai.APIConnectionError as e: #Returns and error and retries if there is an issue communicating with the API
        print(f"\nError communicating with the API.")
        print(f"\nError: {e}") #More detailed error output
        print("\nRetrying...")
        return gpt(conversation_history)

while True:
    request = input("\nEnter request: ")

    if request.lower() == "quit":
        break

    user_prompt = {"role": "user", "content": request}
    conversation_history.append(user_prompt)

    # Generate the response from GPT
    command_to_execute = gpt(conversation_history)  # This should ideally return only the command to execute
    print(f"Executing Command: {command_to_execute}\n")  # Debugging print

    if command_to_execute.strip():  # Check if the command is not empty
        process = subprocess.Popen(command_to_execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, error = process.communicate()

        if error:
            print(f"Error executing command: {error}")

        print(output)

        assistant_response = {"role": "assistant", "content": f"{command_to_execute}\n\n{output}"}
        conversation_history.append(assistant_response)
    else:
        print("No command to execute.")

    # Debug the the conversation history
    # print("Current conversation history:", json.dumps(conversation_history, indent=2))
    

    append_file("command-log.txt", "Request: " + request + "\nCommand: " + command_to_execute + "\nOutput: " + output + "\nError: " + error + "\n\n")




