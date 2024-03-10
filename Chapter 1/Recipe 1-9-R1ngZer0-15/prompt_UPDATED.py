import openai
from openai import OpenAI

client = OpenAI()

def open_file(filepath):
    with open(filepath, 'r', encoding='UTF-8') as infile:
        return infile.read()

def get_chat_gpt_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

openai.api_key = open_file('openai-key.txt')

prompt = open_file("prompt.txt")
response_text = get_chat_gpt_response(prompt)
print(response_text)
