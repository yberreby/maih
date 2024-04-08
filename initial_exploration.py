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
from src.common import *
from src.preprocess import entries

# %%
entries

# %%
# Show distribution of file extensions
# as bar and pie plot.
entries["ext"].value_counts().plot.bar()
plt.title("Distribution of file extensions")
plt.savefig("exts.png")
plt.figure()
entries["ext"].value_counts().plot.pie()
