import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def open_file(filepath):
    with open(filepath, 'r', encoding='UTF-8') as infile:
        return infile.read()

def get_chat_gpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

prompt = open_file("prompt.txt")
response_text = get_chat_gpt_response(prompt)
print(response_text)
