import asyncio
import pyxivapi
import json

import requests

async def example(items:list):
    client = pyxivapi.XIVAPIClient(api_key='c43151f09079460b81b20a18b65e3ab0d6541c6cc6ad4fd4b09c709f544c38d3')
    item_ids = {}
    for item in items:
        response = await client.index_search(
            name = item,
            indexes=["item"],
            columns=['ID'],
            page=0
        )
        item_ids[item] = response["Results"][0]["ID"]
    await client.session.close()
    return item_ids

async def main():
    
    items = ["leather","potion HQ"]
    item_ids = await example(items)
    for item,id in item_ids.items():
        r = requests.get(f'https://universalis.app/api/history/adamantoise/{id}').content
        market_board_history = json.loads(r.decode('utf-8'))
        for entry in market_board_history['entries']:
            if entry['hq'] == ('HQ' in item):
                print(entry)
                break

            # if 'HQ' in item:
            #     if entry['hq']:
            #         print(entry)
            #         break
            # else:
            #     if not entry['hq']:
            #         print(entry)
            #         break
        

if __name__ == "__main__":
    asyncio.run(main())


