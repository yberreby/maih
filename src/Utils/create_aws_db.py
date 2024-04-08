#!/usr/bin/python
import os
import pandas as pd

def create_dataframe_from_folders(base_path):
    """
    Creates a pandas DataFrame from folders and files.
    
    Parameters:
    - base_path: str, the path to the directory containing the folders.
    
    Returns:
    - A pandas DataFrame with two columns: 'Folder Name' and 'Text'.
    """
    folder_names = []
    texts = []
    
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        
        if os.path.isdir(folder_path):
            file_path = os.path.join(folder_path, "rawText.txt")
            
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                
                folder_names.append(folder)
                texts.append(text)
    
    df = pd.DataFrame({
        'name': folder_names,
        'aws_text': texts
    })
    
    return df

base_path = '../../parsed'
df = create_dataframe_from_folders(base_path)

df.to_parquet("../../results/aws_text.parquet")

print(df.head())

