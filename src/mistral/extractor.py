#!/usr/bin/python
import os
import pandas as pd
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import json

# Initialize Mistral Client
api_key = os.environ["MISTRAL_API_KEY"]
client = MistralClient(api_key=api_key)
model = "mistral-large-latest"


def analyze_document(file_path):
    df = pd.read_csv(file_path)
    document_content = df.to_string()

    prompt = """Based on the document, provide concise answers in json format, with the following structure:
{
   "traffic_problems": [
        {
            "place": Name of the place, 
            "traffic_problem": Traffic problems and its nature,
            "start_date": Start date of the problem,
            "end_date": End date of the problem,
            "localization": Localization details (streets or relevant locatition), if there are multiple locations, make several elements,
        },
        ...
    ]
}
Please format your response in JSON.

Document content:
""" + document_content

    messages = [ChatMessage(role="user", content=prompt)]
    chat_response = client.chat(model=model, messages=messages)
    print(chat_response.choices[0].message.content)
    print(json.loads(chat_response.choices[0].message.content))

    # Parsing the structured response into a dictionary
    return json.loads(chat_response.choices[0].message.content)["traffic_problems"]

def process_directory(directory_path='../../parsed_test', result_dir='../../results'):
    ds = []
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file == 'rawText.csv':
                result_dict = analyze_document(os.path.join(root, file))
                for problem in result_dict:
                    ds.append(problem)
    
    results_df = pd.DataFrame.from_records(ds)

    # Ensure the results directory exists
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    
    # Save the DataFrame to a CSV file
    results_path = os.path.join(result_dir, "analysis_results.csv")
    results_df.to_csv(results_path, index=False)
    print(f"Results saved to {results_path}")

if __name__ == "__main__":
    process_directory()
