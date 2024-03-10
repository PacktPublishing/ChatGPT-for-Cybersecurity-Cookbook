import openai
from openai import OpenAI 
import os
import re

client = OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")

# open a souce code file to provide a souce code file as the source_code parameter
with open('source_code.py', 'r') as file:
    source_code = file.read()

def review_code(source_code: str) -> str:
    print(f"Reviewing the source code and adding comments.\n")
    messages = [
        {"role": "system", "content": "You are a seasoned security engineer with extensive experience in reviewing code for potential security vulnerabilities."},
        {"role": "user", "content": f"Please review the following Python source code. Recreate it with helpful and meaningful comments that will help others identify what the code does. Be sure to also include comments for code/lines inside of the functions, where the use/functionality might be more complex Use the hashtag form of comments and not triple quotes. For comments inside of a function place the comments at the end of the corresponding line. For function comments, place them on the line before the function. Souce code:\n\n{source_code}"}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

reviewed_code = review_code(source_code)

# Output the reviewed code to a file called source_code_commented.py
with open('source_code_commented.py', 'w') as file:
    # Remove the initial code block markdown from the response
    reviewed_code = re.sub(r'^```.*\n', '', reviewed_code)
    # Remove the final code block markdown from the response
    reviewed_code = re.sub(r'```$', '', reviewed_code)
    file.write(reviewed_code)

print("The source code has been reviewed and the comments have been added to the file source_code_commented.py")

