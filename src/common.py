from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import tqdm
import pandas as pd

with open("./mistral_api_key", "r") as f:
    mistral_key = f.read()
os.environ["MISTRAL_API_KEY"] = mistral_key