import openai
import os
import subprocess

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
        
def gpt_3(prompt): #Sets up and runs the request to the OpenAI API
    try:
        response = openai.Completion.create(
            model="text-davinci-003", #So far, using davinci-003 works best. Haven't had much luck yet with Ada or Curie
            prompt=prompt,
            temperature=0.1,
            max_tokens=600,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        text = response['choices'][0]['text'].strip() #Trims the API response to be more readable for what we want
        return text
    except openai.APIConnectionError as e: #Returns and error and retries if there is an issue communicating with the API
        print(f"\nError communicating with the API.")
        print(f"\nError: {e}") #More detailed error output
        print("\nRetrying...")
        return gpt_3(prompt)

while True: #Keeps the script running until we issue the "quit" command at the request prompt
    request = input("\nEnter request: ")
    if not request:
        break
    if request == "quit":
        break
    prompt = open_file("prompt4.txt").replace('{INPUT}', request) #Merges our request input with the pre-written prompt file
    command = gpt_3(prompt)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) #Prepares the API response to run in an OS as a command
    print("\n" + command + "\n")
    with process: #Runs the command in the OS and gives real-time feedback
        for line in process.stdout:
            print(line, end='', flush=True)

    exit_code = process.wait()
    append_file("command-log.txt", "Request: " + request + "\nCommand: " + command + "\n\n") #Write the request and GPT generated command to a log
