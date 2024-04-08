import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import json

# Initialize Mistral Client
api_key = os.environ["MISTRAL_API_KEY"]
client = MistralClient(api_key=api_key)
model = "mistral-large-latest"


def extract_semi_structured(txt):
    system = """
Voici le résultat d'un processus d'extraction de texte sur un PDF, extrait d'une base de données d'arrêtés de circulation, de stationnement, ou assimilé.

Informations importantes :
- Certains fichiers sont scannés, d'autres contiennent du texte lisible par ordinateur sans OCR. 
- Il arrive que l'extraction OCR échoue car le fichier n'est pas suffisamment lisible.
- Certains fichiers sont présents de manière inadéquate. Ceux-ci doivent être signalés.
- Plusieurs technologies d'extraction de texte ont été utilisées. Il arrive que l'une fonctionne et l'autre échoue.

Extrais du prochain message utilisateur toute information importante qui t'est présentée, de manière aussi exhaustive que possible.
Attention particulière à :
- tous les détails du lieu concerné, pour l'identifier sans ambiguïté via des APIs géo
- date de début et de fin de la perturbation
Ta réponse sera traitée par un autre modèle afin d'en extraire des données structurées.

Ne répète pas les informations données dans CE message.
Ne répète pas : les références juridiques, les informations concernant les signataires...
Focalise-toi sur les informations pratiques (exhaustivement).
"""

    messages = [
        ChatMessage(role="system", content=system),
        ChatMessage(role="user", content=txt),
    ]
    chat_response = client.chat(model=model, messages=messages)
    return chat_response.choices[0].message.content



def extract_structured(txt):
    system = """
    Use your tool in order to extract structured data from the text given to you in the user message.
    """


    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "extract_structured_traffic_disruption",
                "description": "Get payment status of a transaction",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "array",
                            "description": "Affected locations, formatted as addresses much specificity as possible without risking incorrectness.",
                        },
                        "nature": {
                            "type": "string",
                            "description": "Nature of the traffic disruption",
                        },
                        "start": {
                            "type": "string",
                            "description": "Start date of the disruption, formatted as ISO 8601.",
                        },
                        "end": {
                            "type": "string",
                            "description": "Start date of the disruption, formatted as ISO 8601.",
                        },
                    },
                    "required": ["location", "nature"],
                },
            },
        },
    ]
        
    messages = [
        ChatMessage(role="system", content=system),
        ChatMessage(role="user", content=txt),
    ]
    response = client.chat(model=model, messages=messages, tools=tools,
                           # Force tool use
                           tool_choice="any")
    
    tool_call = response.choices[0].message.tool_calls[0]
    #function_name = tool_call.function.name
    function_params = json.loads(tool_call.function.arguments)
    #print("\nfunction_name: ", function_name, "\nfunction_params: ", function_params)
    return function_params
