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
from src.aws_ocr.pdf_extract import extract_text_from_pdf
import json

# %%
# Run with AWS 

# %%
# %%time
filename = "2002-n°65-Interdiction-aux-vehicules-de-plus-de-35-tonnes-avenue-de-Bordeaux.pdf"
s3BucketName = "textract-console-eu-west-2-cdc481f3-67d6-4bce-ba92-4c6a125d5f8b"
input_text = extract_text_from_pdf(s3BucketName, filename)

# %%
# You can use this to run without AWS key
#aws_txt = pd.read_parquet("results/aws_text.parquet")
#input_text = aws_txt.loc[aws_txt["name"] == "2002-n°65-Interdiction-aux-vehicules-de-plus-de-35-tonnes-avenue-de-Bordeaux"].iloc[0].aws_text

# %%
print(input_text)

# %%
# %%time
ss_txt = extract_semi_structured(input_text)
print(ss_txt)

# %%
# %%time
struct_out = extract_structured(ss_txt)
print(json.dumps(struct_out, indent=4))

# %%
# %%time
from src.Utils.GeoInfo import *
fr_map = geoInfoPipeline(struct_out["location"][0])
fr_map

# %%
