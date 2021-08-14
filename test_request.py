import asyncio
import pyxivapi
import logging

import requests

async def example():
    client = pyxivapi.XIVAPIClient(api_key='c43151f09079460b81b20a18b65e3ab0d6541c6cc6ad4fd4b09c709f544c38d3')

    item = await client.index_search(
        name = "gazelle leather",
        indexes=["item"],
        columns=['ID','Name'],
        page=0

    
    )
    print(item)
    await client.session.close()

def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(example())
    r = requests.get('https://universalis.app/api/adamantoise/19997')
    print(r.content)


