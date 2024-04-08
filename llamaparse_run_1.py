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
from src.lp import parser as lp_parser
from itertools import islice

# %%
import asyncio
async def process_entry(name, entry):
    path = entry.path
    
    doc = None
    exc = None
    try:
        doc = await lp_parser.aload_data(path)
    except Exception as e:
        exc = e
    return name, doc, exc

async def main():
    tasks = []
    #it = islice(entries.iterrows(), 10)
    it = entries.iterrows()
    for name, entry in it:
        task = asyncio.create_task(process_entry(name, entry))
        tasks.append(task)

    results = await asyncio.gather(*tasks, return_exceptions=True)

    print()
    for name, doc, exc in results:
        if exc is not None:
            print(f"Error processing {name}: {exc}")
        else:
            # Process the successfully loaded document
            print(f"Processed {name} successfully")
    return results

# Run the async main function
results = asyncio.run(main())

# %%
len(results)

# %%
results[0]

# %%
# Save as pickle for safety
#import pickle
#with open('ybkey_final_lp_partial.pickle', 'wb') as handle:
#    pickle.dump(results, handle)

with open('ybkey_final_lp_partial.pickle', 'rb') as handle:
    results = pickle.load(handle)

# %%
# Dataframe for ease of handling
df = pd.DataFrame(
    columns=["name", "doc", "exc"],
    data=results
)

# %%
# Successful
df.loc[df["doc"].notna()]

# %%
df

# %%
# Unsuccessful
df.loc[df["doc"].isna()]

# %%
results

# %%
