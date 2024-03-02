import openai
from openai import OpenAI # New import required for the updated API call
import os

def open_file(filepath):
    with open(filepath, 'r', encoding='UTF-8') as infile:
        return infile.read()
    
openai.api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI() # New client initialization required for the updated API call

def get_chat_gpt_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.7
    )
    text = response.choices[0].message.content.strip()
    return text

feed = input("ManPageGPT> $ Enter the name of a tool: ")

prompt = open_file("prompt.txt").replace('<<INPUT>>', feed)

analysis = get_chat_gpt_response(prompt)
print(analysis)

