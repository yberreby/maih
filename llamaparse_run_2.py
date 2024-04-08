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
# %matplotlib widget

# %%
# llama-parse is async-first, running the sync code in a notebook requires the use of nest_asyncio
import nest_asyncio
nest_asyncio.apply()

# %%
from src.common import *
from src.preprocess import entries
from src.lp import process_entries, parser as lp_parser
from itertools import islice
import asyncio

# %%
# Save as pickle for safety
import pickle
#with open('ybkey_final_lp_partial.pickle', 'wb') as handle:
#    pickle.dump(results, handle)

with open('ybkey_final_lp_partial.pickle', 'rb') as handle:
    results = pickle.load(handle)

# Dataframe for ease of handling
df = pd.DataFrame(
    columns=["name", "doc", "exc"],
    data=results
)

missing_names = df.loc[df["doc"].isna()]["name"]
missing_entries = entries.loc[entries.index.isin(missing_names)]

# Run the async main function
new_results = asyncio.run(process_entries(missing_entries))

# %%
new_results

# %%
import pandas as pd
old_df = df
from src.lp import df_from_results
new_df = df_from_results(new_results)
df = new_df

# %%
df

# %%
# Successful
df.loc[df["doc"].notna()]

# %%
# Unsuccessful
df.loc[df["doc"].isna()]

# %%
old_successful = old_df.loc[old_df["doc"].notna()]
new_successful = new_df.loc[new_df["doc"].notna()]
all_successful = pd.concat([old_successful, new_successful])


#with open("lp_all_successful.pickle", "wb") as f:
#    pickle.dump(all_successful, f)

# %%
all_successful

# %%
