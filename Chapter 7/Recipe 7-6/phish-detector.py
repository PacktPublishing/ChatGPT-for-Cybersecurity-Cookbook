import imaplib
import poplib
import email
import openai
import os
from email.header import decode_header

# Initialize the OpenAI API client
openai.api_key = os.getenv("OPENAI_API_KEY")

def call_gpt(prompt):
    messages = [
        {
            "role": "system",
            "content": "You are a cybersecurity expert specialized in detecting phishing emails."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

# Email account details
EMAIL = 'your_email@gmail.com'
APP_PASSWORD = 'your_app_password'  # Use the App Password generated from Gmail
PROTOCOL = 'IMAP'  # Can be 'IMAP' or 'POP'

if PROTOCOL == 'IMAP':
    # Connect using IMAP
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL, APP_PASSWORD)
    mail.select('inbox')
    status, message_numbers = mail.search(None, '(UNSEEN)')
    for num in message_numbers[0].split():
        status, message_data = mail.fetch(num, '(RFC822)')
        for response_part in message_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["subject"])[0]
                from_ = msg.get("from")
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body += part.get_payload(decode=True).decode()
                else:
                    body += msg.get_payload(decode=True).decode()

                # Analyze with ChatGPT
                analysis_result = call_gpt(f"Analyze the following email for signs of phishing:\nSubject: {subject}\nFrom: {from_}\nBody: {body}")
                
                # Print the analysis result
                print(f"Analysis Result for email with subject '{subject}':\n{analysis_result}")
    # Logout from IMAP
    mail.logout()

elif PROTOCOL == 'POP':
    # Connect using POP
    mail = poplib.POP3_SSL('pop.gmail.com')
    mail.user(EMAIL)
    mail.pass_(APP_PASSWORD)
    
    # Get email count
    email_count = len(mail.list()[1])
    
    # Retrieve latest email as an example (can loop through all if needed)
    resp, text, octets = mail.retr(email_count)
    raw_email = b'\r\n'.join(text)
    msg = email.message_from_bytes(raw_email)
    subject, encoding = decode_header(msg["subject"])[0]
    from_ = msg.get("from")
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_payload(decode=True).decode()
    else:
        body += msg.get_payload(decode=True).decode()

    # Analyze with ChatGPT
    analysis_result = call_gpt(f"Analyze the following email for signs of phishing:\nSubject: {subject}\nFrom: {from_}\nBody: {body}")
    
    # Print the analysis result
    print(f"Analysis Result for email with subject '{subject}':\n{analysis_result}")

    # Close POP connection
    mail.quit()
