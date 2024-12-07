import os
from groq import Groq

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_embedding(texts, model="llama3-8b-8192"):
    """
    Get embeddings for the given texts using Groq's model.

    Args:
        texts (list): List of text strings to embed.
        model (str): The model to use for embedding. Defaults to "llama3-8b-8192".

    Returns:
        list: List of embeddings for the input texts.
    """
    # Clean up the text input
    cleaned_texts = [text.replace('\n', ' ').replace('\t', ' ').strip() for text in texts if text]

    # Send request to Groq for embeddings
    embedding_response = client.embeddings.create(
        model=model,
        input=cleaned_texts
    )

    return embedding_response.data

def llm(model="llama3-8b-8192", system_prompt=None, user_prompt=None, assistant_prompt=None, params=None):
    """
    Generate a response using Groq's language model.

    Args:
        model (str): The model to use for generation. Defaults to "llama3-8b-8192".
        system_prompt (str, optional): The system prompt to use.
        user_prompt (str, optional): The user prompt to use.
        assistant_prompt (str, optional): The assistant prompt to use.
        params (dict, optional): Additional parameters for the API call.

    Returns:
        str: The generated response from the language model.
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if assistant_prompt:
        messages.append({"role": "assistant", "content": assistant_prompt})
    if user_prompt:
        messages.append({"role": "user", "content": user_prompt})

    # Send request to Groq API for language model generation
    chat_response = client.chat.completions.create(
        model=model,
        messages=messages,
        **(params if params else {})
    )

    # Extract the content from the response
    try:
        # Extract the content of the message
        response_text = chat_response.choices[0].message.content
        # Return only the actual response, skipping any thinking tags
        response_text = response_text.replace('<thinking>', '').replace('</thinking>', '').strip()
        return response_text
    except (IndexError, KeyError) as e:
        print(f"Error extracting content from response {e}")
        return "No valid response generated"


    # return chat_response.choices[0].message.content
