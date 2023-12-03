import openai

def initialize_openai_client():
    """
    Initialize the OpenAI client with your API key.
    """
    openai.api_key = 'your-api-key'  # Replace with your actual API key
    return openai

def upload_document(client, file_path):
    """
    Uploads a document to OpenAI and returns the file ID.
    """
    response = client.File.create(file_path=file_path, purpose='search')
    return response.id

def create_chat_with_document(client, file_id):
    """
    Create an assistant and a thread for chatting with the document.
    """
    assistant = client.Assistant.create(
        model="gpt-4-1106-preview",
        documents=[file_id]
    )
    assistant_id = assistant["id"]
    thread = client.Thread.create(assistant_id=assistant_id)
    return assistant_id, thread["id"]

def send_message_to_thread(client, assistant_id, thread_id, message):
    """
    Send a message to the assistant in a specific thread.
    """
    response = client.Message.create(
        assistant_id=assistant_id,
        thread_id=thread_id,
        text=message
    )
    return response["data"]["content"]

def main():
    client = initialize_openai_client()
    
    # Upload a cybersecurity standard document
    file_id = upload_document(client, 'path/to/your/cybersecurity-standard.pdf')

    # Create an assistant and thread for document interaction
    assistant_id, thread_id = create_chat_with_document(client, file_id)
    
    while True:
        user_message = input("Ask a question about the cybersecurity standard: ")
        if user_message.lower() == 'exit':
            break

        assistant_response = send_message_to_thread(client, assistant_id, thread_id, user_message)
        print("Assistant:", assistant_response)

if __name__ == "__main__":
    main()
