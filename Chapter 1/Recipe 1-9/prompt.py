import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chat_gpt_response(prompt):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": prompt}],
    max_tokens=2048,
    temperature=0.7
  )
  return response['choices'][0]['message']['content'].strip()

prompt = "Explain the difference between symmetric and asymmetric encryption."
response_text = get_chat_gpt_response(prompt)
print(response_text)

