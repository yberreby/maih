# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
# %load_ext autoreload
# %autoreload 2

# %%
from src.common import *
from src.mistral.mistral_demo import extract_semi_structured, extract_structured

# %%
aws_txt = pd.read_parquet("results/aws_text.parquet")

# %%
input_text = aws_txt.loc[aws_txt["name"] == "prevoyance_rue_40"].iloc[0].aws_text

# %%
print(input_text)

# %%
# %%time
ss_txt = extract_semi_structured(input_text)
print(ss_txt)

# %%
