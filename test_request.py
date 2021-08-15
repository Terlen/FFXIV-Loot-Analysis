import asyncio
import pyxivapi
import json

import requests

async def example():
    client = pyxivapi.XIVAPIClient(api_key='c43151f09079460b81b20a18b65e3ab0d6541c6cc6ad4fd4b09c709f544c38d3')

    item = await client.index_search(
        name = "gazelle leather",
        indexes=["item"],
        columns=['ID'],
        page=0

    
    )
    await client.session.close()
    return item

async def main():
    
    item = await example()
    item_id = item["Results"][0]["ID"]
    r = requests.get(f'https://universalis.app/api/history/adamantoise/{item_id}').content
    
    market_board_history = json.loads(r.decode('utf-8'))
    
    # print(market_board_history)


    # print(market_board_history.keys())
    print(market_board_history['entries'][0])
    # print(datetime.utcfromtimestamp(market_board_history['entries'][0]['timestamp']).strftime('%Y-%m-%d %H:%M:%S'))
    # print(datetime.utcfromtimestamp(market_board_history['entries'][-1]['timestamp']).strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, format='%(message)s')
    asyncio.run(main())


