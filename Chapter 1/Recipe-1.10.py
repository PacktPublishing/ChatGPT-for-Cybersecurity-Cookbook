import openai
import os

def open_file(filepath):
    with open(filepath, 'r', encoding='UTF-8') as infile:
        return infile.read()

openai.api_key = open_file('openai-key.txt')

def get_chat_gpt_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text = response['choices'][0]['text'].strip()
    return text

file = input("Enter a file name: ")
feed = open_file(file)

prompt = open_file("prompt.txt").replace('<<INPUT>>', feed)

analysis = get_chat_gpt_response(prompt)
print(analysis)

