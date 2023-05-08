import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chat_gpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

prompt = "Explain the difference between symmetric and asymmetric encryption."
response_text = get_chat_gpt_response(prompt)
print(response_text)
