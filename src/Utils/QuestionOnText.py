from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def interogateTextWithMistral(text:str,question:str):
    """
    Interrogates a given text with a specified question using the Mistral AI model
    to return a True or False response.

    This function sends a paragraph of text and a related question to the Mistral AI
    chat model. The model is instructed to answer the question with either True or False
    without providing further explanations. 

    Parameters:
    - text (str): A paragraph of text that the question is about.
    - question (str): A question related to the text that requires a True or False answer.

    Returns:
    - str: The model's response, which is either 'True' or 'False'.

    Note:
    - The function uses a predefined API key and model ('mistral-small-latest').
    - The function constructs a conversation flow where the system explains the task to the model,
      followed by the user providing the text and the question.
    - The response is directly extracted from the first choice of the model's chat responses.
    """
    

    api_key = "XosGJQnnWzLLAJjNU7FLJb1p8WVc2ZdM"
    model = "mistral-small-latest"

    client = MistralClient(api_key=api_key)

    messages = [
        ChatMessage(role="system", content="You are given a paragraph of text followed by a question about this text. Answer with just True or False and under no circumpstances do not provide further explainations."),
        ChatMessage(role="user", content="The text is:\n  "+ text),
        ChatMessage(role="user", content="The Question is:\n  "+ question )
    ]

    # No streaming
    chat_response = client.chat(
        model=model,
        messages=messages,
        max_tokens = 1
    )
    return chat_response.choices[0].message.content