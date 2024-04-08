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
    pass