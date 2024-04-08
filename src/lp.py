import os
from llama_parse import LlamaParse
import pandas as pd

# Read LlamaCloud API key - not stored inline for security.
with open("./llamacloud_api_key", "r") as f:
    lc_key = f.read()
os.environ["LLAMA_CLOUD_API_KEY"] = lc_key

parser = LlamaParse(
    api_key=lc_key,  # can also be set in your env as LLAMA_CLOUD_API_KEY
    result_type="markdown",  # "markdown" and "text" are available
    num_workers=9, # if multiple files passed, split in `num_workers` API calls
    verbose=True,
    language="fr"
)


import asyncio
async def process_entry(name, entry):
    path = entry.path
    
    doc = None
    exc = None
    try:
        doc = await parser.aload_data(path)
    except Exception as e:
        exc = e
    return name, doc, exc

async def process_entries(entries):
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


def df_from_results(results):
    import pandas as pd
    return pd.DataFrame(
        columns=["name", "doc", "exc"],
        data=results
    )